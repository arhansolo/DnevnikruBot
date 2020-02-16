import requests
from bs4 import BeautifulSoup
import urllib.request
import asyncio
from pydnevnikruapi.dnevnik import dnevnik
from datetime import datetime

def loginbot(login, password):
    s = requests.Session()
    data = {"exceededAttempts":"False", "ReturnUrl":"", "login": login, "password": password, "Captcha.Input":"", "Captcha.Id":""}
    r = s.post("https://login.dnevnik.ru/login", data=data)
    return s, r.url


def get_personal_inf(login, password):
    login = login
    password = password
    dn = dnevnik.DiaryAPI(login=login, password=password)

    school_id = dn.get_context()["schools"][0]["id"]
    class_id =  dn.get_context()["eduGroups"][0]["id"]
    name = dn.get_context()["firstName"]

    return school_id, class_id, name

def get_timetable_day(date, login, password):
    day = date[0]
    month = date[1]
    year = date[2]

    mas = []

    r1 = loginbot(login=login, password=password)[0].get("https://dnevnik.ru/user/calendar.aspx?year=" + year + "&month=" + month + "&day=" + day)
    soup = BeautifulSoup(r1.text, "html.parser")
    # print(soup)



    # les_n_time_id = soup.findAll('td', class_='nowrap')
    les_id = soup.findAll('div', class_='s3')
    les_lenth = soup.findAll('div', class_='light')
    teachers = soup.findAll('a', class_='u')
    lessons = soup.findAll('p', class_='s2 strong')
    # print(les_n_time_id[1].text)

    for i in range(len(les_id)):
        try:
            if lessons[i].find('a') is not None\
                    and teachers[i] is not None and les_id[i] is not None and les_lenth[i] is not None:
                #print(les_id[i].text + ":", lessons[i].text ,  '(' + les_lenth[i].text + ')' ',', teachers[i].text)
                mas.append(les_id[i].text + ": " +  lessons[i].text +  ' (' + les_lenth[i].text + ')' ', ' + teachers[i].text)
        except IndexError:
            if lessons[i].find('a') is not None\
                    and teachers[i] is not None and les_id[i] is not None:
                #print(les_id[i].text + ":", lessons[i].text + ',', teachers[i].text)
                mas.append(les_id[i].text + ": " + lessons[i].text + ', ' + teachers[i].text)
    return mas

def get_calls(login, password):
    r2 = loginbot(login=login, password=password)[0].get('https://schools.dnevnik.ru/schedules/view.aspx?school=' +
                                                         str(get_personal_inf(login=login, password=password)[0]) + '&group=' +str(get_personal_inf(login=login, password=password)[1])+'&tab=timetable')
    soup = BeautifulSoup(r2.text, "html.parser")

    get_calls_mas = []
    call_mas = []
    day_mas = []

    table_call = soup.findAll('table', class_='grid vam')
    #time = soup.findAll('td', class_='tac s3')
    #les_num = soup.findAll('td', class_='tac')

    day = soup.findAll('ul', class_='moder')

    for i in range(len(table_call)):
        if table_call[i] is not None and day[i].find('h3'):
            call_mas.append(table_call[i].text.replace('\n', " ").replace("   ", '\n').strip())
            day_mas.append(day[i].text)
            #print(day[i].text, table_call[i].text.replace('\n', " ").replace("   ", '\n').strip(), sep="\n")
    get_calls_mas.append(day_mas)
    get_calls_mas.append(call_mas)
    return get_calls_mas



def get_hm_week(login, password):
    r2 = loginbot(login=login, password=password)[0].get(
        'https://schools.dnevnik.ru/homework.aspx')
    soup = BeautifulSoup(r2.text, "html.parser")
    mas = []

    subjects = soup.findAll('td', class_='tac light')
    homework = soup.findAll('td', class_='breakword')
    date = soup.findAll('td', class_='tac nowrap')

    for i in range(len(date)):
        if subjects[i] is not None and homework[i].find('a') is not None and date[i].find('strong') is not None and i == 0:
            #print(subjects[i].text.strip() + ":", homework[i].text.strip() + ",", "выполнить к " + date[i].find('strong').text.strip())
            mas.append(subjects[i].text.strip() + ": " + homework[i].text.strip() + ", " + "выполнить к " + date[i].find('strong').text.strip())
        else:
            #print(subjects[i * 2].text.strip() + ":", homework[i].text.strip() + ",", "выполнить к " + date[i].find('strong').text.strip())
            mas.append(subjects[i * 2].text.strip() + ": " + homework[i].text.strip() + ", " + "выполнить к " + date[i].find('strong').text.strip())
    return mas


'''
def get_marks(login, password):
    data = {"_ga": "GA1.2.1298295227.1580831060", "_gat": "1", "_gat_schools": "1", "_gid": 'GA1.2.621150714.1580831060', "_ym_d": "1580831060",
            "_ym_isad": "2", "_ym_uid": "1580831060160769294", "a_r_p_i": "163.2", "dnevnik_sst": "9f9e0704-c317-4f50-8389-7e4bb08bcc4e|05.02.2020 14:55:47", "DnevnikAuth_a": 'QTJOV4pVK8rGwHc/BwMjbgoQo5YzD6mdvGrHHqSGsoqWXBQYQzt1sK/ThRX6wnmDUHn7j+AZmp86ltq9MG5OmFxBpA4wFvrOIMsr8JKm2Ql3rZzU+WJ8DpfmKCqaRO+IfdiwUGpN0a1roJTm/pYppsNBSWVKapdAou0RWTOt7MFZcY+su/p2awWEawC/WN9YgXl8xvDNXyhGoHUFko/4bfCHPhA=',
            "t0": "1000005527431"}
    r2 = loginbot(login=login, password=password)[0].post(
        'https://schools.dnevnik.ru/marks.aspx?school=1000005527431&index=2&tab=period&homebasededucation=False', data = data)
    soup = BeautifulSoup(r2.text, "html.parser")
    print(soup)
'''



#get_timetable_day("30.01.2020")
#print(get_calls("", ""))
#get_hm_week(login="", password="")
#print(get_personal_inf("", ""))


#get_marks()

