import requests
from bs4 import BeautifulSoup
import feedparser
import sqlite3

from datetime import date, timedelta

yesterday = (date.today() - timedelta(1)).strftime('%Y/%m/%d')
today = (date.today()).strftime('%Y/%m/%d')


def getWeather():
    location = '충청남도 논산시' + '날씨'
    LocationInfo = ""

    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + location
    hdr = {'User-Agent': (
        'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.70 '
        'safari/537.36')}

    req = requests.get(url, headers=hdr)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    week = soup.find('div', {'class': 'table_info weekly _weeklyWeather'})

    weather: str = ""
    for elem in week.find_all('li', {'class': 'date_info today'}):
        weather += ' '.join((str(elem.get_text()) + '<br>').split())

    return weather


def getSciNews_tech():
    f = feedparser.parse('https://www.sciencetimes.co.kr/category/sci-tech/feed/')

    str_list = []
    for feed in f['entries']:
        str_list.append(str(feed.title) + '<br>' + str(feed.description) + '<br><br>')

    message = ''.join(str_list)

    return message


def getSciNews_policy():
    f = feedparser.parse('https://www.sciencetimes.co.kr/category/sci-policy/feed/')

    str_list = []
    for feed in f['entries']:
        str_list.append(str(feed.title) + '<br>' + str(feed.description) + '<br><br>')

    message = ''.join(str_list)

    return message


def getSciNews_culture():
    f = feedparser.parse('https://www.sciencetimes.co.kr/category/sci-culture/feed/')

    str_list = []
    for feed in f['entries']:
        str_list.append(str(feed.title) + '<br>' + str(feed.description) + '<br><br>')

    message = ''.join(str_list)

    return message


def getNews_tongil():
    f = feedparser.parse('http://www.tongilnews.com/rss/allArticle.xml')

    str_list = []
    for feed in f['entries']:
        str_list.append(str(feed.title) + '<br>' + str(feed.description) + '<br><br>')

    message = ''.join(str_list)

    return message


def getTelegramMessage():
    try:
        dbConn = sqlite3.connect('Message.db')
        dbCur = dbConn.cursor()


        query = "SELECT NAME, MESSAGE FROM MESSAGE WHERE DATE='{}'".format(yesterday)
        history = dbCur.execute(query).fetchall()
        message = str(yesterday)
        for i in history:
            j = str(i).replace(',', ' ')
            j = str(j).replace('(', '')
            j = str(j).replace(')', '')
            j = str(j).replace("'", '')
            message += "\n" + "<br><br>" + j


        query = "SELECT NAME, MESSAGE FROM MESSAGE WHERE DATE='{}'".format(today)
        history = dbCur.execute(query).fetchall()
        message += '<br><br>' + str(today)
        for i in history:
            j = str(i).replace(',', ' ')
            j = str(j).replace('(', '')
            j = str(j).replace(')', '')
            j = str(j).replace("'", '')
            message += "\n" + "<br><br>" + j

        dbConn.close()
        return message
    except Exception as e:
        print(e)
