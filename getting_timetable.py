import datetime


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


# Функция находит какая пара будет следующей
def indicate_next_lesson(timetable):
    current_date_time = datetime.datetime.now()  # Текущая дата
    day = dictionary_days[current_date_time.weekday()]  # Текущий день
    current_time = current_date_time.time()
    hour = int(current_time.hour)  # Текущий час
    minute = int(current_time.minute)  # Текущая минута
    time_of_lesson = ""
    output = []
    k = 1

    while len(output) == 0:
        # Цикл по всем парам
        for lesson in timetable:
            if lesson['day'] == day and k == 1:  # Ищем в текущем дне следующую пару
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
    current_date_time = datetime.datetime.now()  # Текущая дата
    day = dictionary_days[current_date_time.weekday()]
    current_time = current_date_time.time()
    hour = int(current_time.hour)
    minute = int(current_time.minute)
    output = []
    time_of_lesson = ""

    for lesson in timetable:
        if lesson['day'] == day:
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