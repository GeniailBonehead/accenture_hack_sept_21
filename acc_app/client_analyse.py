from collections import Counter

stable_act = ['ОФЗ 26219',
            'ОФЗ 26215',
            'ОФЗ 26222',
            'Сбербанк',
            'Газпром',
            'ВТБ',
            'Apple',
            'Microsoft',
            'Amazon']

aggressive_act = [
    'Virgin Galactic',
    'Tesla',
    'Zoom',
    'TAL',
    'Twilio',
    'Okta',
    'DocuSign',
    'Upwork',
    'Etsy',
]

middle_act = [
    'Распадская',
    'QIWI',
    'Башнефть',
    'Moderna',
    'Carnival',
    'Cronos Group',
    'America Airlines',
    'Delta',
    'Alibaba',
]
price = 753

mock = {}


class Client:
    def __init__(self):
        self.portfolio = {}

    def buy(self, name, price, amount):
        if name not in self.portfolio:
            self.portfolio['name'] = {}
            self.portfolio['name']['money'] = 0.0
            self.portfolio['name']['amount'] = 0
        self.portfolio['name']['money'] += price
        self.portfolio['name']['amount'] += 1

    def sell(self, stock, amount):
        self.portfolio -= Counter({stock: amount})


def analyse_client(portfolio):
    agr_style = 0
    all = 0
    passive_style = 0
    for stock in portfolio.items():
        all += portfolio[stock] * price
        if stock in stable_act:
            passive_style += portfolio[stock] * price
        if stock in aggressive_act:
            agr_style += portfolio[stock] * price

    aggressiveness = agr_style / all
    return aggressiveness


# mock = {'Газпром': {'money': 100500, 'amount': 20}, 'rger': {'money': 100500, 'amount': 20}}
# data = []
# for x in mock.items():
#     data.append({'name': x[0], 'money': x[1]['money'], 'amount': x[1]['amount']})
# # data = [x.index(), x.value() for ]
# print(data)