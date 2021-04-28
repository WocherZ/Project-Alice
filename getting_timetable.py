import datetime
import pytz


# Удаление пробелов перед числом
def delete_zeros(str_number):
    t = []
    check = False
    for i in str_number:
        if i != "0":
            check = True
        if check:
            t.append(i)
    if len(t) == 0:
        return "0"
    else:
        return "".join(t)


# Разбиение времени на часы и минуты
def split_time(time_str):
    t1 = []
    t2 = []
    check = True
    for i in time_str:
        if i == ":":
            check = False
        elif check:
            t1.append(i)
        elif check is False:
            t2.append(i)
    return [delete_zeros("".join(t1)), delete_zeros("".join(t2))]


# Время начала пары
def start_time(time_str):
    t = []
    check = True
    for i in time_str:
        if i == " " or i == "-":
            check = False
        elif check:
            t.append(i)
        elif check is False:
            break
    return split_time("".join(t))


# Время окончания пары
def end_time(time_str):
    t = []
    check = False
    for i in time_str:
        if i == " " or i == "-":
            check = True
        elif check:
            t.append(i)
        elif check is False:
            pass
    return split_time("".join(t[1: len(t)]))


# GLOBAL
dictionary_days = {0: "Понедельник",
                   1: "Вторник",
                   2: "Среда",
                   3: "Четверг",
                   4: "Пятница",
                   5: "Суббота",
                   6: "Воскресенье"}

parity_week = {0: "Четная неделя", 1: "Нечетная неделя", 2: "Еженедельно"}


def check_parity_week(date):
    start_session = datetime.datetime(year=2021, month=2, day=8, hour=0, minute=0)

    delta = date - start_session
    delta_days = delta.days
    count_weeks = (delta_days // 7) + 1  # Какая неделя по счёту
    if count_weeks % 2 == 0:
        return parity_week[0]
    else:
        return parity_week[1]


# Функция находит какая пара будет следующей
def indicate_next_lesson(timetable):
    # current_date_time = datetime.datetime(year=2021, month=4, day=20, hour=13, minute=0)  # Текущая дата
    current_date_time = datetime.datetime.now(pytz.timezone('Europe/Moscow')).replace(tzinfo=None)
    day = dictionary_days[current_date_time.weekday()]  # Текущий день
    current_time = current_date_time.time()
    hour = int(current_time.hour)  # Текущий час
    minute = int(current_time.minute)  # Текущая минута
    week = check_parity_week(current_date_time)  # Текущая неделя: чётная или нечётная
    time_of_lesson = ""
    output = []
    k = 1


    while len(output) == 0:

        if day == "Воскресенье":
            if week == parity_week[0]:
                week = parity_week[1]
            elif week == parity_week[1]:
                week = parity_week[0]

        # Цикл по всем парам
        for lesson in timetable:
            if lesson['day'] == day and k == 1:  # Ищем в текущем дне следующую пару
                if lesson["weekly"] == week or lesson["weekly"] == parity_week[2]:
                    lesson_start_time = start_time(lesson["time"])  # Время начала пары

                    # Если час совпадает с часом пары, то сравниваем минуты
                    if hour == int(lesson_start_time[0]):
                        if minute <= int(lesson_start_time[1]):

                            if time_of_lesson == lesson["time"]:
                                output.append(lesson)
                            if not time_of_lesson:
                                output.append(lesson)
                                time_of_lesson = lesson["time"]

                    # Если час пары больше текущего часа
                    elif hour < int(lesson_start_time[0]):

                        if time_of_lesson == lesson["time"]:
                            output.append(lesson)
                        if not time_of_lesson:
                            output.append(lesson)
                            time_of_lesson = lesson["time"]

            if lesson['day'] == day and k != 1:  # Ищем в следующих днях первую пару если не нашли в текущем дне
                if time_of_lesson == lesson["time"]:
                    output.append(lesson)
                if not time_of_lesson:
                    output.append(lesson)
                    time_of_lesson = lesson["time"]


        # Если цикл не нашёл следующей пары в текущем дне
        if len(output) == 0:
            day = dictionary_days[(current_date_time.weekday() + k) % 7]  # Изменяем день на следующий
            k += 1

    return output


# Функция находит какая пара сейчас
def indicate_current_lesson(timetable):
    # current_date_time = datetime.datetime(year=2021, month=4, day=23, hour=12, minute=50)  # Текущая дата
    current_date_time = datetime.datetime.now(pytz.timezone('Europe/Moscow')).replace(tzinfo=None)
    day = dictionary_days[current_date_time.weekday()]
    current_time = current_date_time.time()
    hour = int(current_time.hour)
    minute = int(current_time.minute)
    week = check_parity_week(current_date_time)  # Текущая неделя: чётная или нечётная
    output = []
    time_of_lesson = ""

    for lesson in timetable:
        if lesson['day'] == day:
            if lesson["weekly"] == week or lesson["weekly"] == parity_week[2]:
                lesson_start_time = start_time(lesson["time"])
                lesson_end_time = end_time(lesson["time"])

                if int(lesson_start_time[0]) <= hour <= int(lesson_end_time[0]):
                    if hour == int(lesson_start_time[0]):
                        if minute >= int(lesson_start_time[1]):

                            if time_of_lesson == lesson["time"]:
                                output.append(lesson)
                            if not time_of_lesson:
                                output.append(lesson)
                                time_of_lesson = lesson["time"]

                    elif hour == int(lesson_end_time[0]):
                        if minute <= int(lesson_end_time[1]):

                            if time_of_lesson == lesson["time"]:
                                output.append(lesson)
                            if not time_of_lesson:
                                output.append(lesson)
                                time_of_lesson = lesson["time"]

                    elif int(lesson_start_time[0]) < hour < int(lesson_end_time[0]):

                        if time_of_lesson == lesson["time"]:
                            output.append(lesson)
                        if not time_of_lesson:
                            output.append(lesson)
                            time_of_lesson = lesson["time"]


    return output


# Функция находит какие пары сегодня
def indicate_today_lesson(timetable):
    current_date_time = datetime.datetime.now(pytz.timezone('Europe/Moscow')).replace(tzinfo=None)  # Текущая дата
    day = dictionary_days[current_date_time.weekday()]
    week = check_parity_week(current_date_time)  # Текущая неделя: чётная или нечётная

    output = []
    for lesson in timetable:
        if lesson['day'] == day:
            if lesson["weekly"] == week or lesson["weekly"] == parity_week[2]:
                output.append(lesson)

    return output


# Функция находит какие пары завтра
def indicate_tomorrow_lesson(timetable):
    # current_date_time = datetime.datetime(year=2021, month=4, day=23, hour=12, minute=50) # Текущая дата
    current_date_time = datetime.datetime.now(pytz.timezone('Europe/Moscow')).replace(tzinfo=None)  # Текущая дата
    day = dictionary_days[(current_date_time.weekday() + 1) % 7]
    week = check_parity_week(current_date_time)  # Текущая неделя: чётная или нечётная

    if day == "Воскресенье":
        if week == parity_week[0]:
            week = parity_week[1]
        else:
            week = parity_week[0]

    output = []
    for lesson in timetable:
        if lesson['day'] == day:
            if lesson["weekly"] == week or lesson["weekly"] == parity_week[2]:
                output.append(lesson)

    return output


# Функция находит какие пары в понедельник
def indicate_monday_lesson(timetable):
    day = dictionary_days[0]
    output = []
    for lesson in timetable:
        if lesson['day'] == day:
            output.append(lesson)

    return output


# Функция находит какие пары во вторник
def indicate_tuesday_lesson(timetable):
    day = dictionary_days[1]
    output = []
    for lesson in timetable:
        if lesson['day'] == day:
            output.append(lesson)

    return output


# Функция находит какие пары в среду
def indicate_wednesday_lesson(timetable):
    day = dictionary_days[2]
    output = []
    for lesson in timetable:
        if lesson['day'] == day:
            output.append(lesson)

    return output


# Функция находит какие пары в четверг
def indicate_thursday_lesson(timetable):
    day = dictionary_days[3]
    output = []
    for lesson in timetable:
        if lesson['day'] == day:
            output.append(lesson)

    return output


# Функция находит какие пары в пятницу
def indicate_friday_lesson(timetable):
    day = dictionary_days[4]
    output = []
    for lesson in timetable:
        if lesson['day'] == day:
            output.append(lesson)

    return output


# Функция находит какие пары в субботу
def indicate_saturday_lesson(timetable):
    day = dictionary_days[5]
    output = []
    for lesson in timetable:
        if lesson['day'] == day:
            output.append(lesson)

    return output


# Функция находит какие пары в воскресенье
def indicate_sunday_lesson(timetable):
    day = dictionary_days[6]
    output = []
    for lesson in timetable:
        if lesson['day'] == day:
            output.append(lesson)

    return output


