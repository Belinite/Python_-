import requests
import webbrowser
url1 = "https://www.reformagkh.ru/search/houses?query="


# для записи данных страницы в файл
def search(address):
    webbrowser.open(url1 + address)
    url2 = url1 + address
    print(url2)
    r = requests.get(url2)
    print(r)
    with open('test.html', 'w') as output_file:
        output_file.write(r.text)
    link = read_file()
    return link


# для получения ссылки
def read_file():
    with open('test.html') as input_file:
        text = input_file.read()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(text, "lxml")
        class_list = soup.find('div', {'class': 'grid'})
        n = 'None'
        if class_list == n:
            class_list2 = 0
            return class_list2
        else:
            class_list2 = class_list.find('a').get('href')
            return class_list2


# получение кода страницы
def common(house):
    r = requests.get(house)
    with open('questionnaire.html', 'w') as output_file:
        output_file.write(r.text)


# отыскание нужных объектов на странице
def read_file_questionnaire(filename):
    ret = []  # некая переменная для добавления нужных элементов
    with open(filename) as input_file:
        text = input_file.read()
        results = []
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(text, "lxml")
        last_update = soup.find_all('section', {'class': 'house_info clearfix'})
        for update in last_update:
            n = update.find_all('table', {'class': 'col_list_group'})
            for nn in n:
                nnn = nn.find_all('span')
                for nnnn in nnn:
                    word = nnnn.text
                    results.append(word)
        class_list = soup.find_all('div', {'class': 'tab'})
        for item in class_list:
            new_name = item.find('th', {'style': 'text-align:center'})
            new = (item.find('td', {'style': 'padding: 10px;'}))#поиск кадастрового номера
            number = new.text
            name_of_number = new_name.text
            items2 = item.find_all('span')
            for itemss in items2:
                article = itemss.text
                results.append(
                    article
                )
            elems = item.find_all('div', {'class': 'subtab'})
            for pp in elems:
                elems2 = pp.find_all('span')
                for elems3 in elems2:
                    article2 = elems3.text
                    results.append(
                        article2
                    )
                    results = list(results)
                    from numpy import array
                    resultss = array(results)
                    for r in resultss:
                        indx = list(resultss).index(r)
                        if r == 'Год ввода дома в эксплуатацию':
                            year = resultss[indx + 1]
                        elif r == 'наибольшее, ед.':
                            floor = resultss[indx + 1]
                        elif r == 'Серия, тип постройки здания':
                            type_of_building = resultss[indx + 1]
                        elif r == 'Тип дома':
                            type_of_house = resultss[indx + 1]
                        elif r == 'Дом признан аварийным':
                            accident = resultss[indx + 1]
                        elif r == 'Тип перекрытий':
                            floor_type = resultss[indx + 1]
                        elif r == 'Материал несущих стен':
                            walls = resultss[indx + 1]
                            walls = str(walls).replace(',', '/')
                        elif r == 'Последнее изменение анкеты':
                            last = resultss[indx + 1]
                    cadastral = number

        ret.append(year)
        ret.append(floor)
        ret.append(type_of_building)
        ret.append(type_of_house)
        ret.append(accident)
        ret.append(floor_type)
        ret.append(walls)
        ret.append(cadastral)
        ret.append(last)
        return ret


# считывание данных с базы данных и запись в файл
def read_from_mssql():
    with open('C:/Users/user/Desktop/сайт питон/r.csv', 'w', encoding='utf-16') as output_file:
        result = list()
        new = []
        from sqlalchemy import create_engine
        engine = create_engine("mssql+pymssql://логин:пароль@айпи:порт/название бд")# Вставить свои данные для подключения к бд
        connection = engine.connect()
        connection.execute('insert_into_search')
        tr_list = connection.execute("SELECT Address FROM for_search")
        for tr in tr_list:
            result.append(tr)  # список
        for r in result:
            for s in r:
                spl = s.split(',')
                for sp in spl:
                    import re
                    match = re.findall(r'(кв. \w+)', sp)
                    ind_sp = 0
                    for m in match:
                        ind_sp = spl.index(sp)
                    indx_sp = list(spl).index(sp)
                    if indx_sp == 0:
                        spl.remove(spl[0])
                    elif indx_sp == ind_sp:
                        spl.remove(spl[ind_sp])
                for_s = ", ".join(spl)
                new.append(for_s)
        tr_par = connection.execute("SELECT Address_Region FROM for_search")
        for n in new:
            print(n)
            i = 0
            try:
                link = search(n)
                print(link)
                webbrowser.open("https://www.reformagkh.ru" + link)
                house = "https://www.reformagkh.ru" + link
                common(house)
                ret = read_file_questionnaire('questionnaire.html')
                d = str(ret).replace('[', '')
                d = d.replace(']', '')
                d = d.replace('\'', '')
                d = d.replace('               ', '')
                d = d.replace('\\n', '')
                d = d.replace('            ', '')
                d = d.replace('   ', '')
                output_file.write(d + '\n')
            except Exception:
                output_file.write(str('Неверный адрес') + ',')
                output_file.write(str('Неверный адрес') + ',')
                output_file.write(str('Неверный адрес') + ',')
                output_file.write(str('Неверный адрес') + ',')
                output_file.write(str('Неверный адрес') + ',')
                output_file.write(str('Неверный адрес') + ',')
                output_file.write(str('Неверный адрес') + ',')
                output_file.write(str('Неверный адрес') + ',')
                output_file.write(str('Неверный адрес') + '\n')


        connection.close()


def proc(): #определить количество объектов для Материал несущих стен = Кирпичный по каждому региону.
    res = []
    res2 = []
    num = 0
    from sqlalchemy import create_engine
    engine = create_engine("mssql+pymssql://логин:пароль@айпи:порт/название бд")# Вставить свои данные для подключения к бд
    connection = engine.connect()
    tr_list = connection.execute("select Address_Region from new_table where Material_of_bearing_walls='Каменные/ кирпичные'")
    for tt in tr_list:
        res.append(tt)
    for ttt in res:
        if ttt in res2:
            num += 1
        else:
            num = 1
        res2.append(ttt)
        res2.append(num)
    for result in res2:
        print(result)


def show_results_of_search():
    from sqlalchemy import create_engine
    engine = create_engine("mssql+pymssql://логин:пароль@айпи:порт/название бд")# Вставить свои данные для подключения к бд
    connection = engine.connect()
    tr_list = connection.execute("select Floor_of_house from new_table")
    found = 0
    not_found = 0
    res = []
    for tt in tr_list:
        print(tt)
        d = str(tt).replace('\'', '')
        d = d.replace(',', '')
        d = d.replace('(', '')
        d = d.replace(')', '')
        res.append(d)
    for result in res:
        if result == 'Неверный адрес':
            not_found += 1
        else:
            found += 1
    print('Количество найденных объектов: ' + str(found))
    print('Количество не найденных объектов: ' + str(not_found))


# основная функция, которая вызывает остальные
def working_with_db():
    read_from_mssql()
    from sqlalchemy import create_engine
    engine = create_engine("mssql+pymssql://логин:пароль@айпи:порт/название бд")# Вставить свои данные для подключения к бд
    connection = engine.connect()
    connection.execute('insert_into_result')
    proc()
    show_results_of_search()
    connection.execute('delete_from_for_search') # очищение бд
    connection.execute('delete_from_results') # очищение бд
    connection.close()


working_with_db()










