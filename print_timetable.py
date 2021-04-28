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
    return ["".join(t1), "".join(t2)]


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


def print_help():
    text = "Этот навык поможет тебе узнать расписание. Дай мне знать свою группу и я скажу тебе расписание."
    return text


# Функция возвращает текст с содержанием следующей пары
def print_next_lesson(timetable):
    start = start_time(timetable[0]["time"])[0] + ":" + start_time(timetable[0]["time"])[1]
    text = "Следующее занятие в " + start + ": " + "\n"
    lesson = timetable
    for element in lesson:
        subject = element["name subject"] + "\n"
        text += subject

    return text


# Функция возвращает текст с содержанием текущей пары
def print_current_lesson(timetable):
    if len(timetable) != 0:
        end = end_time(timetable[0]["time"])[0] + ":" + end_time(timetable[0]["time"])[1]
        text = "Сейчас:" + "\n"
        text += timetable[0]["name subject"]
        text += " до " + str(end)
    else:
        text = "В данный момент у тебя нет занятий"
    return text


# Функция возвращает текст с содержанием сегодняшних пар
def print_today_lesson(timetable):
    if timetable:
        text = "Сегодня у тебя следующие занятия:" + "\n"
        for lesson in timetable:
            row = lesson["time"] + " " + lesson["name subject"] + "\n"
            text += row
    else:
        text = "Сегодня у тебя нет занятий"
    return text


# Функция возвращает текст с содержанием пар на завтра
def print_tomorrow_lesson(timetable):
    if timetable:
        text = "Завтра у тебя следующие занятия:" + "\n"
        for lesson in timetable:
            row = lesson["time"] + " " + lesson["name subject"] + "\n"
            text += row
    else:
        text = "Завтра у тебя нет занятий"
    return text


def print_monday_lesson(timetable):
    if timetable:
        text = "В понедельник у тебя следующие занятия:" + "\n"
        for lesson in timetable:
            row = lesson["time"] + " " + lesson["name subject"] + "\n"
            text += row
    else:
        text = "В понедельник у тебя нет занятий"
    return text


def print_tuesday_lesson(timetable):
    if timetable:
        text = "Во вторник у тебя следующие занятия:" + "\n"
        for lesson in timetable:
            row = lesson["time"] + " " + lesson["name subject"] + "\n"
            text += row
    else:
        text = "Во вторник у тебя нет занятий"
    return text


def print_wednesday_lesson(timetable):
    if timetable:
        text = "В среду у тебя следующие занятия:" + "\n"
        for lesson in timetable:
            row = lesson["time"] + " " + lesson["name subject"] + "\n"
            text += row
    else:
        text = "В среду у тебя нет занятий"
    return text


def print_thursday_lesson(timetable):
    if timetable:
        text = "В четверг у тебя следующие занятия:" + "\n"
        for lesson in timetable:
            row = lesson["time"] + " " + lesson["name subject"] + "\n"
            text += row
    else:
        text = "В четверг у тебя нет занятий"
    return text


def print_friday_lesson(timetable):
    if timetable:
        text = "В пятницу у тебя следующие занятия:" + "\n"
        for lesson in timetable:
            row = lesson["time"] + " " + lesson["name subject"] + "\n"
            text += row
    else:
        text = "В пятницу у тебя нет занятий"
    return text


def print_saturday_lesson(timetable):
    if timetable:
        text = "В субботу у тебя следующие занятия:" + "\n"
        for lesson in timetable:
            row = lesson["time"] + " " + lesson["name subject"] + "\n"
            text += row
    else:
        text = "В субботу у тебя нет занятий"
    return text


def print_sunday_lesson(timetable):
    if timetable:
        text = "В воскресенье у тебя следующие занятия:" + "\n"
        for lesson in timetable:
            row = lesson["time"] + " " + lesson["name subject"] + "\n"
            text += row
    else:
        text = "В воскресение у тебя нет занятий"
    return text

# print(print_next_lesson(test_datetime.indicate_next_lesson(test_datetime.group_timetable)))
# print(print_current_lesson(test_datetime.indicate_current_lesson(test_datetime.group_timetable)))
# print(print_today_lesson(test_datetime.indicate_today_lesson(test_datetime.group_timetable)))
# print(print_tomorrow_lesson(test_datetime.indicate_tomorrow_lesson(test_datetime.group_timetable)))

