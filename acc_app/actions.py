# -*- coding: utf-8 -*-

DATABASE = '/var/www/u0733193/data/www/venisoking.ru/mapwars/warApp/actions.db'
import sqlite3
import requests
from bs4 import BeautifulSoup
import json
from django.core.mail import EmailMessage
from django.core.mail import send_mail

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}


def get_actions():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = "select * from actions"
    cursor.execute(sql)
    sqlResult = cursor.fetchall()
    conn.close()
    res = []
    for line in sqlResult:
        dict_line = dict()
        dict_line['name'], dict_line['last'], dict_line['max_price'], dict_line['min_price'], \
        dict_line['change'], dict_line['perc_change'], dict_line['amount'], dict_line['data_time'] = line
        res.append(dict_line)
    return res


def get_actions_online(site='https://ru.investing.com/equities/most-active-stocks', short=False):
    html = requests.get(site, headers=headers)
    bsObj = BeautifulSoup(html.content, "lxml")
    table = bsObj.find('div', id='stockPageInnerContent')
    lines = table.find_all('tr')
    data = []
    for line in lines[1:]:
        dict_line = dict()
        addit_data = line.find_all('td')[1].find('span')
        # l = [x.text for x in line.find_all('td')]
        _, dict_line['name'], dict_line['last'], dict_line['max_price'], dict_line['min_price'], \
        dict_line['change'], dict_line['perc_change'], dict_line['amount'], dict_line['data_time'], _ = \
            [x.text for x in line.find_all('td')]
        dict_line['data_id'] = addit_data.get('data-id')
        dict_line['link'] = line.find('a').get('href')
        dict_line['short_link'] = dict_line['link'].replace('/equities/', '')
        amount = 0
        if 'M' in dict_line['amount']:
            amount = float(dict_line['amount'][:-1].replace(',', '.')) * 1000000
        elif 'B' in dict_line['amount']:
            amount = float(dict_line['amount'][:-1].replace(',', '.')) * 1000000000
        elif 'K' in dict_line['amount']:
            amount = float(dict_line['amount'][:-1].replace(',', '.')) * 1000
        else:
            amount = float(dict_line['amount'].replace(',', '.'))
        # print(amount, dict_line['amount'])
        dict_line['max_price'] = float(dict_line['max_price'].replace('.', '').replace(',', '.'))
        dict_line['min_price'] = float(dict_line['min_price'].replace('.', '').replace(',', '.'))
        dict_line['last'] = float(dict_line['last'].replace('.', '').replace(',', '.'))
        dict_line['amount'] = amount
        dict_line['alarm'] = 0
        perc = dict_line['perc_change'][1:-1].replace(',', '.')

        if (float(perc) > 4):
            if dict_line['perc_change'][0] == '+':
                dict_line['alarm'] = 1
                dict_line['res'] = 'up'
            else:
                dict_line['alarm'] = 2
                dict_line['res'] = 'down'
        elif short:
            continue
        data.append(dict_line)
    return data


def get_charts(data_id):
    site = "https://advcharts.investing.com/advinion2016/advanced-charts/7/7/18/GetRecentHistory?strSymbol={}&iTop=1500&strPriceType=bid&strFieldsMode=allFields&strExtraData=lang_ID=7&strTimeFrame=1D".format(data_id)
    responce = requests.get(site, headers=headers).content
    responce = str(responce)[2:-1]
    data = json.loads(responce)
    for line in data["data"]:
        line["high"] = str(line["high"]).replace(',', '.')
        line["low"] = str(line["low"]).replace(',', '.')
    return data

def get_stats(link):
    site = "https://ru.investing.com" + link + "-ratios"
    html = requests.get(site, headers=headers)
    bsObj = BeautifulSoup(html.content, "lxml")
    block = bsObj.find(id='childTr')
    table = block.find('table')
    res = []
    for line in table.find_all('tr'):
        name, value, value_comm = [td.text for td in line.find_all('td')]
        res.append({
            'name': name,
            'value': value,
            'value_comm': value_comm,
        })
    return res

def get_money(link):
    site = "https://ru.investing.com" + link + "-income-statement"
    html = requests.get(site, headers=headers)
    bsObj = BeautifulSoup(html.content, "lxml")
    block = bsObj.find(id='childTr')
    res = []
    for line in block.find_all('tr'):
        name, val1, val2, val3, val4 = [td.text for td in line.find_all('td')]
        if val1 == '-':
            val1 = '0'
        if val2 == '-':
            val2 = '0'
        if val3 == '-':
            val3 = '0'
        if val4 == '-':
            val4 = '0'
        res.append({'name': name,
                    'val1': val1,
                    'val2': val2,
                    'val3': val3,
                    'val4': val4})
    block = bsObj.find(id='rrtable').find('table')
    naming = [th.text for th in block.find('tr').find_all('th')]
    for line in block.find_all('tr')[10:]:
        name, val1, val2, val3, val4 = [td.text for td in line.find_all('td')]
        if val1 == '-':
            val1 = '0'
        if val2 == '-':
            val2 = '0'
        if val3 == '-':
            val3 = '0'
        if val4 == '-':
            val4 = '0'
        res.append({'name': name,
                    'val1': val1,
                    'val2': val2,
                    'val3': val3,
                    'val4': val4})
    return res, naming


def send_message():
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    password = 'password'

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('dstrannik10@gmail.com', password)
    text = """Возможно, Вам стоит обратить внимание на свой портфель акций.
    
    
Отчёт подготовлен командой Цикличность действий для кейса accenture"""
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = Header('Акции требуют Вашего внимания', 'utf-8')
    msg['From'] = "dstrannik10@gmail.com"
    msg['To'] = "dstrannikfake@gmail.com"

    smtpObj.sendmail("dstrannik10@gmail.com", "dstrannikfake@gmail.com", msg.as_string())
    smtpObj.quit()

# data = get_actions_online(short=True)
# for line in data:
#     print(line)


def get_valute():
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    for line in data['Valute'].values():
        if float(line['Value']) > float(line['Previous']):
            line['up'] = 'up'
        else:
            line['up'] = 'down'
    return data['Valute']


# Cкользящая средняя, берет 20 последних данных цен и делит на их количество
def sma(data, n):
    sum = 0
    for i in range(n):
        sum = sum + data["data"][i]["close"] # сумма цен закрытия
    return sum / n # арифметическое среднее цен закрытия


# Теханализ, если последняя цена больше, чем скользящая средняя, то возвращает рекомендацию на покупку (1),
# если цена меньше, на продажу (-1), иначе нейтрально (0)
def techanaliz():
    data = get_charts(13683) # словарь котировок
    last_cost = data["data"][0]["close"]  # получили последнюю цену закрытия
    sm = sma(data, 20) # передаем котировки
    if last_cost > sm:
        return 1
    elif last_cost < sm:
        return -1
    else:
        return 0

