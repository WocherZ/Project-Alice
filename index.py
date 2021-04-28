import parsing_timetable
import getting_timetable
import print_timetable

STATE_REQUEST_KEY = 'session'
STATE_RESPONSE_KEY = 'session_state'


def make_response(text, tts=None, state=None):
    response = {
        'text': text,
        'tts': tts if tts is not None else text,
    }
    webhook_response = {
        'response': response,
        'version': '1.0',
    }
    if state is not None:
        webhook_response[STATE_RESPONSE_KEY] = state
    return webhook_response


def welcome_message(event):
    text = ('Привет! Я - это тестовый навык расписания! Я могу тебе сказать расписание. Какая у тебя группа?')
    return make_response(text)


def ask_group(event, state=None):
    text = 'Для начала мне надо знать какая у тебя группа'
    return make_response(text, state=state)


def what_you_want(event, state=None):
    text = 'Что хотите узнать из расписания?'
    return make_response(text, state=state)


# Следующее занятие
def get_next_lesson(group, state=None):
    lessons = getting_timetable.indicate_next_lesson(state["group_timetable"])
    text = print_timetable.print_next_lesson(lessons)
    return make_response(text, state=state)


# Текущее занятие
def get_current_lesson(group, state=None):
    lessons = getting_timetable.indicate_current_lesson(state["group_timetable"])
    text = print_timetable.print_current_lesson(lessons)
    return make_response(text, state=state)


# Занятия сегодня
def get_today_lesson(group, state=None):
    lessons = getting_timetable.indicate_today_lesson(state["group_timetable"])
    text = print_timetable.print_today_lesson(lessons)
    return make_response(text, state=state)


# Занятия завтра
def get_tomorrow_lesson(group, state=None):
    lessons = getting_timetable.indicate_tomorrow_lesson(state["group_timetable"])
    text = print_timetable.print_tomorrow_lesson(lessons)
    return make_response(text, state=state)


# Занятия в понедельник
def get_monday_lesson(group, state=None):
    lessons = getting_timetable.indicate_monday_lesson(state["group_timetable"])
    text = print_timetable.print_monday_lesson(lessons)
    return make_response(text, state=state)


# Занятия во вторник
def get_tuesday_lesson(group, state=None):
    lessons = getting_timetable.indicate_tuesday_lesson(state["group_timetable"])
    text = print_timetable.print_tuesday_lesson(lessons)
    return make_response(text, state=state)


# Занятия в среду
def get_wednesday_lesson(group, state=None):
    lessons = getting_timetable.indicate_wednesday_lesson(state["group_timetable"])
    text = print_timetable.print_wednesday_lesson(lessons)
    return make_response(text, state=state)


# Занятия в четверг
def get_thursday_lesson(group, state=None):
    lessons = getting_timetable.indicate_thursday_lesson(state["group_timetable"])
    text = print_timetable.print_thursday_lesson(lessons)
    return make_response(text, state=state)


# Занятия в пятницу
def get_friday_lesson(group, state=None):
    lessons = getting_timetable.indicate_friday_lesson(state["group_timetable"])
    text = print_timetable.print_friday_lesson(lessons)
    return make_response(text, state=state)


# Занятия в субботу
def get_saturday_lesson(group, state=None):
    lessons = getting_timetable.indicate_saturday_lesson(state["group_timetable"])
    text = print_timetable.print_saturday_lesson(lessons)
    return make_response(text, state=state)


# Занятия в воскресенье
def get_sunday_lesson(group, state=None):
    lessons = getting_timetable.indicate_sunday_lesson(state["group_timetable"])
    text = print_timetable.print_sunday_lesson(lessons)
    return make_response(text, state=state)


# Сообщение об ошибке
def fallback(event, state=None):
    text = 'Извините, я вас не понял. Пожалуйста попробуйте ещё раз'
    return make_response(text, state=state)


# Сообщение помощник
def help_message():
    text = print_timetable.print_help()
    return text


# Функция - обработчик запроса пользователя
def get_user_request(request, group_timetable):
    if request == 'help':
        text = help_message
    elif request == 'get_next_lesson':
        text = print_timetable.print_next_lesson(getting_timetable.indicate_next_lesson(group_timetable))
    elif request == 'get_current_lesson':
        text = print_timetable.print_current_lesson(getting_timetable.indicate_current_lesson(group_timetable))
    elif request == 'get_today_lesson':
        text = print_timetable.print_today_lesson(getting_timetable.indicate_today_lesson(group_timetable))
    elif request == 'get_tomorrow_lesson':
        text = print_timetable.print_tomorrow_lesson(getting_timetable.indicate_tomorrow_lesson(group_timetable))
    elif request == 'get_monday_lesson':
        text = print_timetable.print_monday_lesson(getting_timetable.indicate_monday_lesson(group_timetable))
    elif request == 'get_tuesday_lesson':
        text = print_timetable.print_tuesday_lesson(getting_timetable.indicate_tuesday_lesson(group_timetable))
    elif request == 'get_wednesday_lesson':
        text = print_timetable.print_wednesday_lesson(getting_timetable.indicate_wednesday_lesson(group_timetable))
    elif request == 'get_thursday_lesson':
        text = print_timetable.print_thursday_lesson(getting_timetable.indicate_thursday_lesson(group_timetable))
    elif request == 'get_friday_lesson':
        text = print_timetable.print_friday_lesson(getting_timetable.indicate_friday_lesson(group_timetable))
    elif request == 'get_saturday_lesson':
        text = print_timetable.print_saturday_lesson(getting_timetable.indicate_saturday_lesson(group_timetable))
    elif request == 'get_sunday_lesson':
        text = print_timetable.print_sunday_lesson(getting_timetable.indicate_sunday_lesson(group_timetable))
    else:
        text = 'Я не смогла распознать твой запрос'

    return text


# Функция распознования интентов
def identify_intents(intents):
    if 'help' in intents:
        return 'help'
    elif 'get_next_lesson' in intents:
        return 'get_next_lesson'
    elif 'get_current_lesson' in intents:
        return 'get_current_lesson'
    elif 'get_today_lesson' in intents:
        return 'get_today_lesson'
    elif 'get_tomorrow_lesson' in intents:
        return 'get_tomorrow_lesson'
    elif 'get_monday_lesson' in intents:
        return 'get_monday_lesson'
    elif 'get_tuesday_lesson' in intents:
        return 'get_tuesday_lesson'
    elif 'get_wednesday_lesson' in intents:
        return 'get_wednesday_lesson'
    elif 'get_thursday_lesson' in intents:
        return 'get_thursday_lesson'
    elif 'get_friday_lesson' in intents:
        return 'get_friday_lesson'
    elif 'get_saturday_lesson' in intents:
        return 'get_saturday_lesson'
    elif 'get_sunday_lesson' in intents:
        return 'get_sunday_lesson'
    else:
        return ""


# ГЛАВНАЯ ФУНКЦИЯ - ОБРАБОТЧИК ЗАПРОСОВ
def handler(event, context):
    intents = event['request'].get('nlu', {}).get('intents')
    state = event.get('state').get(STATE_REQUEST_KEY, {})

    # Если сессия только запущена то выдаём приветственное сообщение
    if event['session']['new']:
        return welcome_message(event)

    elif 'help' in intents:
        text = help_message()
        return make_response(text, state=state)

    # Если пользователь назвал свою группу
    elif 'get_group_name' in intents:
        state['name_group'] = event['request'].get('original_utterance')  # Записываем в state группу
        timetable = parsing_timetable.parser(state['name_group'])  # Парсим расписание
        state['group_timetable'] = timetable  # Записываем расписание

        # Если пользователь отправлял до этого какой-либо запрос
        if state.get('last_user_request'):

            # В зависимости от запроса отправляем ему расписание
            request = state['last_user_request']
            text = get_user_request(request, state.get('group_timetable'))
            state['last_user_request'] = None
            return make_response(text, state=state)

        # Если пользователь не отправлял ещё запрос - то спрашиваем что он хочет
        else:
            return what_you_want(event, state)

    # Если мы знаем группу то действуем в соответствии с запросом пользователя
    elif state.get('name_group'):

        # Если пользователь отправлял до этого какой-либо запрос
        if state.get('last_user_request'):
            # В зависимости от запроса отправляем ему расписание
            request = state['last_user_request']
            text = get_user_request(request, state.get('group_timetable'))
            state['last_user_request'] = None
            return make_response(text, state=state)

        # Если пользователь прямо сейчас отправил запрос
        elif intents:  # В intents точно не лежит имя группы(т.к. до этого была проверка)
            request = list(intents.keys())[0]
            text = get_user_request(request, state.get('group_timetable'))
            state['last_user_request'] = None
            return make_response(text, state=state)

        # Если пользователь не отправлял ещё запрос - то спрашиваем что он хочет
        else:
            return what_you_want(event, state)

        # Дальше будут рассмотрены другие случаи...

    # Если мы не знаем группу - то спрашиваем её
    elif not state.get('name_group'):

        # Проверка на то является ли сообщение запросом расписания
        if intents:
            request = identify_intents(intents)
            state['last_user_request'] = request

            return ask_group(event, state)
        else:
            return fallback(event)


    # Если это не подходит не под один из запросов то выдаём ошибку
    else:
        return fallback(event)