import requests
from bs4 import BeautifulSoup
import urllib.request



def loginbot(login, password):
    s = requests.Session()
    data = {"exceededAttempts":"False", "ReturnUrl":"", "login": login, "password": password, "Captcha.Input":"", "Captcha.Id":""}
    r = s.post("https://login.dnevnik.ru/login", data=data)
    return s, r.url



