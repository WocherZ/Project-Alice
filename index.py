import parsing_timetable
import getting_timetable

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


def get_next_lesson(group, state=None):
    text = "Следующее занятие: " + "\n"
    lesson = getting_timetable.indicate_next_lesson(state["group_timetable"])
    for element in lesson:
        subject = element["name subject"] + "\n"
        text += subject

    return make_response(text, state=state)


def get_current_lesson(group, state=None):
    lesson = getting_timetable.indicate_current_lesson(state["group_timetable"])
    if len(lesson) != 0:
        text = "Сейчас у тебя:" + "\n"
        for element in lesson:
            subject = element["name subject"] + "\n"
            text += subject

        text += lesson[0]["time"]

        return make_response(text, state=state)
    else:
        text = "У тебя сейчас нет пары"
        return make_response(text, state=state)


def fallback(event, state=None):
    text = 'Извините, я вас не понял. Пожалуйста попробуйте ещё раз'
    return make_response(text, state=state)


def help_message(event, state=None):
    text = "Я могу тебе подсказать расписание. Для мне надо всего лишь знатьгруппу."
    return make_response(text, state=state)


# ГЛАВНАЯ ФУНКЦИЯ - ОБРАБОТЧИК ЗАПРОСОВ
def handler(event, context):
    intents = event['request'].get('nlu', {}).get('intents')
    state = event.get('state').get(STATE_REQUEST_KEY, {})

    # Если сессия только запущена то выдаём приветственное сообщение
    if event['session']['new']:
        return welcome_message(event)

    if 'help' in intents:
        return help_message(event, state=state)

    # Если пользователь назвал свою группу
    elif 'get_group_name' in intents:
        state['name_group'] = event['request'].get('original_utterance')  # Записываем в state группу
        timetable = parsing_timetable.parser(state['name_group'])  # Проблема с парсингом
        state['group_timetable'] = timetable

        # Если пользователь отправлял до этого какой-либо запрос
        if state.get('last_user_request'):

            # В зависимости от запроса отправляем ему расписание
            if state['last_user_request'] == 'get_next_lesson':
                return get_next_lesson(state.get('name_group'), state)
            if state['last_user_request'] == 'get_current_lesson':
                return get_current_lesson(state.get('name_group'), state)

            else:
                return make_response("Затычка 1", state=state)

        # Если пользователь не отправлял ещё запрос - то спрашиваем что он хочет
        else:
            return what_you_want(event, state)

    # Если мы знаем группу то действуем в соответствии с запросом пользователя
    elif state.get('name_group'):

        # Если пользователь отправлял до этого какой-либо запрос
        if state.get('last_user_request'):
            if state['last_user_request'] == 'get_next_lesson':
                return get_next_lesson(state.get('name_group'), state)
            if state['last_user_request'] == 'get_current_lesson':
                return get_current_lesson(state.get('name_group'), state)

        # Если пользователь прямо сейчас отправил запрос
        elif intents:  # В intents точно не лежит имя группы(т.к. до этого была проверка)
            if 'get_next_lesson' in intents:
                return get_next_lesson(state.get('name_group'), state)
            if 'get_current_lesson' in intents:
                return get_current_lesson(state.get('name_group'), state)


        # Если пользователь не отправлял ещё запрос - то спрашиваем что он хочет
        else:
            return what_you_want(event, state)

        # Дальше будут рассмотрены другие случаи...

    # Если мы не знаем группу - то спрашиваем её
    elif not state.get('name_group'):

        # Проверка на то является ли сообщение запросом расписания
        if intents:
            if 'get_next_lesson' in intents:
                state['last_user_request'] = 'get_next_lesson'
            if 'get_current_lesson' in intents:
                state['last_user_request'] = 'get_current_lesson'

            return ask_group(event, state)
        else:
            return fallback(event)


    # Если это не подходит не под один из запросов то выдаём ошибку
    else:
        return fallback(event)