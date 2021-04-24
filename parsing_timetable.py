import requests
from bs4 import BeautifulSoup


def get_html(url, params=''):
    r = requests.get(url, params=params)
    return r


def selection_text(string):
    out = []
    check_tag = False
    if string[0] == "<":
        check_tag = True
    for el in string:
        if el == "<":
            check_tag = True
        elif check_tag is False:
            out.append(el)
        elif el == ">":
            check_tag = False
    return ''.join(out)


def delete_commas(string):
    out = []
    for i in string:
        if i != ',':
            out.append(i)
    return ''.join(out)


def get_name_subject(html):
    in_tag = False  # Всё что в тэге
    check_tag = False  # Проверка на открытие и закрытие тэга
    string = str(html)
    output = []
    answer = []
    if string[0] == "<":
        check_tag = True

    for i in range(len(string)):
        if check_tag is False and in_tag is False and string[i] != "<" and string[i] != ">":
            output.append(string[i])
        if string[i] == "<":
            check_tag = True  # Вход в тэг
            in_tag = True
            if string[i + 1] == "/":
                in_tag = False  # Тэг закрывается
        elif string[i] == ">":
            check_tag = False  # Выход из тэга

    for j in output:
        if 32 <= ord(j) <= 126 or 1040 <= ord(j) <= 1103:
            answer.append(j)

    return ''.join(answer)


def selection_day(string):
    out = []
    for j in string:
        if j != "\n" and j != "[" and j != "]" and j != " ":
            out.append(j)
    return "".join(out)


def get_group_name(string):
    answer = []
    start_word = "группы"
    index = string.find(start_word)
    if index != -1:
        for i in range(index + len(start_word), len(string)):
            if string[i] != "\n":
                answer.append(string[i])
    return ''.join(answer)


def processing(group):
    return group.upper()


def get_content(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', {"id": "page-content-wrapper"})
    output = []
    number_day = 0
    list_group_days = []

    for item in items:
        group = item.find('h1', class_='light')  # название группы
        name_group = get_group_name(selection_text(str(group)))  # Группа
        days = selection_text(str(item.find_all('h3', class_='lesson-wday')))  # дни недели   Не работает get text
        for d in days.split(","):
            m = selection_day(d)
            list_group_days.append(m)

        lists_of_lessons = item.find_all('div', class_='list-group')  # расписание по дням

        for list_of_day in lists_of_lessons:  # list_of_day - расписание одного дня
            day = list_group_days[number_day]
            number_day += 1
            lessons = list_of_day.find_all('div', class_='list-group-item')

            for lesson in lessons:  # lesson - одна пара
                time_lesson = lesson.find('div', class_='lesson-time').get_text(strip=True).replace('\xa0',
                                                                                                    ' ')  # время пары(строка)
                subject = lesson.find_all('div', class_='lesson')  # дисциплины на этой паре

                for sub in subject:
                    name_of_sub = delete_commas(get_name_subject(sub))  # дисциплина
                    type_of_sub = selection_text(
                        str(sub.find('div', class_='label label-default label-lesson')))  # тип занятия
                    teacher = selection_text(str(sub.find_all('a', class_='text-nowrap')))[1: -1]
                    weekly = str(sub.find("span", class_="lesson-square")["title"])  # Еженедельность

                    output.append(
                        {
                            'group': name_group,
                            'name subject': name_of_sub,
                            'day': day,
                            'time': time_lesson,
                            'type': type_of_sub,
                            'weekly': weekly,
                            'teacher': teacher
                        }
                    )
    return output


def parser(group):
    GROUPS_URLS = {'Б20-101': 'https://home.mephi.ru/study_groups/11122/schedule',
                   'Б20-102': 'https://home.mephi.ru/study_groups/11123/schedule',
                   'Б20-103': 'https://home.mephi.ru/study_groups/11124/schedule',
                   'Б20-104': 'https://home.mephi.ru/study_groups/11125/schedule',
                   'Б20-105': 'https://home.mephi.ru/study_groups/11126/schedule',
                   'Б20-161': 'https://home.mephi.ru/study_groups/11127/schedule',
                   'Б20-163': 'https://home.mephi.ru/study_groups/11128/schedule',
                   'Б20-201': 'https://home.mephi.ru/study_groups/11129/schedule',
                   'Б20-202': 'https://home.mephi.ru/study_groups/11130/schedule',
                   'Б20-203': 'https://home.mephi.ru/study_groups/11131/schedule',
                   'Б20-204': 'https://home.mephi.ru/study_groups/11132/schedule',
                   'Б20-205': 'https://home.mephi.ru/study_groups/11133/schedule',
                   'Б20-211': 'https://home.mephi.ru/study_groups/11134/schedule',
                   'Б20-215': 'https://home.mephi.ru/study_groups/11135/schedule',
                   'Б20-261': 'https://home.mephi.ru/study_groups/11136/schedule',
                   'Б20-263': 'https://home.mephi.ru/study_groups/11137/schedule',
                   'Б20-265': 'https://home.mephi.ru/study_groups/11138/schedule',
                   'Б20-291': 'https://home.mephi.ru/study_groups/11139/schedule',
                   'Б20-292': 'https://home.mephi.ru/study_groups/11140/schedule',
                   'Б20-293': 'https://home.mephi.ru/study_groups/11141/schedule',
                   'Б20-301': 'https://home.mephi.ru/study_groups/11142/schedule',
                   'Б20-302': 'https://home.mephi.ru/study_groups/11143/schedule',
                   'Б20-312': 'https://home.mephi.ru/study_groups/11144/schedule',
                   'Б20-361': 'https://home.mephi.ru/study_groups/11145/schedule',
                   'Б20-362': 'https://home.mephi.ru/study_groups/11146/schedule',
                   'Б20-392': 'https://home.mephi.ru/study_groups/11147/schedule',
                   'Б20-401': 'https://home.mephi.ru/study_groups/11148/schedule',
                   'Б20-402': 'https://home.mephi.ru/study_groups/11149/schedule',
                   'Б20-403': 'https://home.mephi.ru/study_groups/11150/schedule',
                   'Б20-413': 'https://home.mephi.ru/study_groups/11151/schedule',
                   'Б20-461': 'https://home.mephi.ru/study_groups/11152/schedule',
                   'Б20-462': 'https://home.mephi.ru/study_groups/11153/schedule',
                   'Б20-463': 'https://home.mephi.ru/study_groups/11154/schedule',
                   'Б20-464': 'https://home.mephi.ru/study_groups/11155/schedule',
                   'Б20-465': 'https://home.mephi.ru/study_groups/11156/schedule',
                   'Б20-503': 'https://home.mephi.ru/study_groups/11157/schedule',
                   'Б20-504': 'https://home.mephi.ru/study_groups/11158/schedule',
                   'Б20-505': 'https://home.mephi.ru/study_groups/11159/schedule',
                   'Б20-513': 'https://home.mephi.ru/study_groups/11160/schedule',
                   'Б20-514': 'https://home.mephi.ru/study_groups/11161/schedule',
                   'Б20-515': 'https://home.mephi.ru/study_groups/11162/schedule',
                   'Б20-523': 'https://home.mephi.ru/study_groups/11163/schedule',
                   'Б20-524': 'https://home.mephi.ru/study_groups/11164/schedule',
                   'Б20-561': 'https://home.mephi.ru/study_groups/11165/schedule',
                   'Б20-563': 'https://home.mephi.ru/study_groups/11166/schedule',
                   'Б20-564': 'https://home.mephi.ru/study_groups/11167/schedule',
                   'Б20-565': 'https://home.mephi.ru/study_groups/11168/schedule',
                   'Б20-593': 'https://home.mephi.ru/study_groups/11169/schedule',
                   'Б20-601': 'https://home.mephi.ru/study_groups/11170/schedule',
                   'Б20-602': 'https://home.mephi.ru/study_groups/11171/schedule',
                   'Б20-603': 'https://home.mephi.ru/study_groups/11172/schedule',
                   'Б20-604': 'https://home.mephi.ru/study_groups/11173/schedule',
                   'Б20-611': 'https://home.mephi.ru/study_groups/11174/schedule',
                   'Б20-661': 'https://home.mephi.ru/study_groups/11175/schedule',
                   'Б20-701': 'https://home.mephi.ru/study_groups/11176/schedule',
                   'Б20-702': 'https://home.mephi.ru/study_groups/11177/schedule',
                   'Б20-703': 'https://home.mephi.ru/study_groups/11178/schedule',
                   'Б20-763': 'https://home.mephi.ru/study_groups/11179/schedule',
                   'Б20-801': 'https://home.mephi.ru/study_groups/11180/schedule',
                   'Б20-802': 'https://home.mephi.ru/study_groups/11181/schedule',
                   'Б20-901': 'https://home.mephi.ru/study_groups/11182/schedule',
                   'Б20-902': 'https://home.mephi.ru/study_groups/11183/schedule',
                   'Б20-В01': 'https://home.mephi.ru/study_groups/11184/schedule',
                   'Б20-В02': 'https://home.mephi.ru/study_groups/11185/schedule',
                   'Б20-В03': 'https://home.mephi.ru/study_groups/11186/schedule',
                   'Б20-В71': 'https://home.mephi.ru/study_groups/11187/schedule',
                   'Б19-101': 'https://home.mephi.ru/study_groups/11074/schedule',
                   'Б19-102': 'https://home.mephi.ru/study_groups/11075/schedule',
                   'Б19-103': 'https://home.mephi.ru/study_groups/11076/schedule',
                   'Б19-104': 'https://home.mephi.ru/study_groups/11077/schedule',
                   'Б19-105': 'https://home.mephi.ru/study_groups/11078/schedule',
                   'Б19-161': 'https://home.mephi.ru/study_groups/11079/schedule',
                   'Б19-162': 'https://home.mephi.ru/study_groups/11080/schedule',
                   'Б19-163': 'https://home.mephi.ru/study_groups/11081/schedule',
                   'Б19-165': 'https://home.mephi.ru/study_groups/11082/schedule',
                   'Б19-166': 'https://home.mephi.ru/study_groups/11083/schedule',
                   'Б19-167': 'https://home.mephi.ru/study_groups/11084/schedule',
                   'Б19-168': 'https://home.mephi.ru/study_groups/11085/schedule',
                   'Б19-201': 'https://home.mephi.ru/study_groups/11086/schedule',
                   'Б19-202': 'https://home.mephi.ru/study_groups/11087/schedule',
                   'Б19-203': 'https://home.mephi.ru/study_groups/11088/schedule',
                   'Б19-204': 'https://home.mephi.ru/study_groups/11089/schedule',
                   'Б19-205': 'https://home.mephi.ru/study_groups/11090/schedule',
                   'Б19-211': 'https://home.mephi.ru/study_groups/11091/schedule',
                   'Б19-301': 'https://home.mephi.ru/study_groups/11092/schedule',
                   'Б19-302': 'https://home.mephi.ru/study_groups/11093/schedule',
                   'Б19-401': 'https://home.mephi.ru/study_groups/11094/schedule',
                   'Б19-402': 'https://home.mephi.ru/study_groups/11095/schedule',
                   'Б19-403': 'https://home.mephi.ru/study_groups/11096/schedule',
                   'Б19-501': 'https://home.mephi.ru/study_groups/11097/schedule',
                   'Б19-503': 'https://home.mephi.ru/study_groups/11098/schedule',
                   'Б19-504': 'https://home.mephi.ru/study_groups/11099/schedule',
                   'Б19-505': 'https://home.mephi.ru/study_groups/11100/schedule',
                   'Б19-511': 'https://home.mephi.ru/study_groups/11101/schedule',
                   'Б19-513': 'https://home.mephi.ru/study_groups/11102/schedule',
                   'Б19-514': 'https://home.mephi.ru/study_groups/11103/schedule',
                   'Б19-515': 'https://home.mephi.ru/study_groups/11104/schedule',
                   'Б19-525': 'https://home.mephi.ru/study_groups/11105/schedule',
                   'Б19-565': 'https://home.mephi.ru/study_groups/11106/schedule',
                   'Б19-601': 'https://home.mephi.ru/study_groups/11107/schedule',
                   'Б19-602': 'https://home.mephi.ru/study_groups/11108/schedule',
                   'Б19-603': 'https://home.mephi.ru/study_groups/11109/schedule',
                   'Б19-604': 'https://home.mephi.ru/study_groups/11110/schedule',
                   'Б19-701': 'https://home.mephi.ru/study_groups/11111/schedule',
                   'Б19-702': 'https://home.mephi.ru/study_groups/11112/schedule',
                   'Б19-801': 'https://home.mephi.ru/study_groups/11113/schedule',
                   'Б19-802': 'https://home.mephi.ru/study_groups/11114/schedule',
                   'Б19-803': 'https://home.mephi.ru/study_groups/11115/schedule',
                   'Б19-901': 'https://home.mephi.ru/study_groups/11116/schedule',
                   'Б19-902': 'https://home.mephi.ru/study_groups/11117/schedule',
                   'Б19-В01': 'https://home.mephi.ru/study_groups/11118/schedule',
                   'Б19-В02': 'https://home.mephi.ru/study_groups/11119/schedule',
                   'Б19-В03': 'https://home.mephi.ru/study_groups/11120/schedule',
                   'Б19-В71': 'https://home.mephi.ru/study_groups/11121/schedule',
                   'Б18-101': 'https://home.mephi.ru/study_groups/11042/schedule',
                   'Б18-102': 'https://home.mephi.ru/study_groups/11043/schedule',
                   'Б18-103': 'https://home.mephi.ru/study_groups/11044/schedule',
                   'Б18-104': 'https://home.mephi.ru/study_groups/11045/schedule',
                   'Б18-105': 'https://home.mephi.ru/study_groups/11046/schedule',
                   'Б18-106': 'https://home.mephi.ru/study_groups/11047/schedule',
                   'Б18-201': 'https://home.mephi.ru/study_groups/11048/schedule',
                   'Б18-202': 'https://home.mephi.ru/study_groups/11049/schedule',
                   'Б18-203': 'https://home.mephi.ru/study_groups/11050/schedule',
                   'Б18-204': 'https://home.mephi.ru/study_groups/11051/schedule',
                   'Б18-211': 'https://home.mephi.ru/study_groups/11052/schedule',
                   'Б18-301': 'https://home.mephi.ru/study_groups/11053/schedule',
                   'Б18-302': 'https://home.mephi.ru/study_groups/11054/schedule',
                   'Б18-402': 'https://home.mephi.ru/study_groups/11055/schedule',
                   'Б18-403': 'https://home.mephi.ru/study_groups/11056/schedule',
                   'Б18-501': 'https://home.mephi.ru/study_groups/11057/schedule',
                   'Б18-502': 'https://home.mephi.ru/study_groups/11058/schedule',
                   'Б18-503': 'https://home.mephi.ru/study_groups/11059/schedule',
                   'Б18-504': 'https://home.mephi.ru/study_groups/11060/schedule',
                   'Б18-505': 'https://home.mephi.ru/study_groups/11061/schedule',
                   'Б18-513': 'https://home.mephi.ru/study_groups/11062/schedule',
                   'Б18-514': 'https://home.mephi.ru/study_groups/11063/schedule',
                   'Б18-565': 'https://home.mephi.ru/study_groups/11064/schedule',
                   'Б18-601': 'https://home.mephi.ru/study_groups/11065/schedule',
                   'Б18-602': 'https://home.mephi.ru/study_groups/11066/schedule',
                   'Б18-701': 'https://home.mephi.ru/study_groups/11067/schedule',
                   'Б18-702': 'https://home.mephi.ru/study_groups/11068/schedule',
                   'Б18-801': 'https://home.mephi.ru/study_groups/11069/schedule',
                   'Б18-В01': 'https://home.mephi.ru/study_groups/11070/schedule',
                   'Б18-В02': 'https://home.mephi.ru/study_groups/11071/schedule',
                   'Б18-В71': 'https://home.mephi.ru/study_groups/11072/schedule',
                   'Б18-В73': 'https://home.mephi.ru/study_groups/11073/schedule',
                   'Б17-101': 'https://home.mephi.ru/study_groups/11009/schedule',
                   'Б17-102': 'https://home.mephi.ru/study_groups/11010/schedule',
                   'Б17-103': 'https://home.mephi.ru/study_groups/11011/schedule',
                   'Б17-105': 'https://home.mephi.ru/study_groups/11012/schedule',
                   'Б17-106': 'https://home.mephi.ru/study_groups/11013/schedule',
                   'Б17-201': 'https://home.mephi.ru/study_groups/11014/schedule',
                   'Б17-202': 'https://home.mephi.ru/study_groups/11015/schedule',
                   'Б17-203': 'https://home.mephi.ru/study_groups/11016/schedule',
                   'Б17-211': 'https://home.mephi.ru/study_groups/11017/schedule',
                   'Б17-212': 'https://home.mephi.ru/study_groups/11018/schedule',
                   'Б17-221': 'https://home.mephi.ru/study_groups/11019/schedule',
                   'Б17-301': 'https://home.mephi.ru/study_groups/11020/schedule',
                   'Б17-391': 'https://home.mephi.ru/study_groups/11021/schedule',
                   'Б17-401': 'https://home.mephi.ru/study_groups/11022/schedule',
                   'Б17-402': 'https://home.mephi.ru/study_groups/11023/schedule',
                   'Б17-403': 'https://home.mephi.ru/study_groups/11024/schedule',
                   'Б17-501': 'https://home.mephi.ru/study_groups/11025/schedule',
                   'Б17-502': 'https://home.mephi.ru/study_groups/11026/schedule',
                   'Б17-503': 'https://home.mephi.ru/study_groups/11027/schedule',
                   'Б17-504': 'https://home.mephi.ru/study_groups/11028/schedule',
                   'Б17-505': 'https://home.mephi.ru/study_groups/11029/schedule',
                   'Б17-511': 'https://home.mephi.ru/study_groups/11030/schedule',
                   'Б17-514': 'https://home.mephi.ru/study_groups/11031/schedule',
                   'Б17-515': 'https://home.mephi.ru/study_groups/11032/schedule',
                   'Б17-565': 'https://home.mephi.ru/study_groups/11033/schedule',
                   'Б17-592': 'https://home.mephi.ru/study_groups/11034/schedule',
                   'Б17-594': 'https://home.mephi.ru/study_groups/11035/schedule',
                   'Б17-601': 'https://home.mephi.ru/study_groups/11036/schedule',
                   'Б17-701': 'https://home.mephi.ru/study_groups/11037/schedule',
                   'Б17-801': 'https://home.mephi.ru/study_groups/11038/schedule',
                   'Б17-901': 'https://home.mephi.ru/study_groups/11039/schedule',
                   'Б17-В01': 'https://home.mephi.ru/study_groups/11040/schedule',
                   'Б17-В02': 'https://home.mephi.ru/study_groups/11041/schedule',
                   'Б16-В03': 'https://home.mephi.ru/study_groups/11008/schedule'}
    group = processing(group)
    url = GROUPS_URLS[group]
    html = get_html(url)
    if html.status_code == 200:
        data = get_content(html)
        return data
    else:
        return []