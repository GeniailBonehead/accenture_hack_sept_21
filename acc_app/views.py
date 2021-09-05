from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .actions import *
from .client_analyse import mock
from django.core.cache import cache


def acc_last_buy_online(request):
    site = 'https://ru.investing.com/equities/most-active-stocks'
    res = get_actions_online(site)
    response = HttpResponse(str(res).replace("'", '"'), content_type="application/json; charset=utf-8")
    #response = JsonResponse(res, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    response['Content-Type'] = 'application/json; charset=utf-8'
    return response


def last_buy_nice(request):
    site = 'https://ru.investing.com/equities/most-active-stocks'
    res = get_actions_online(site)
    return render(request, 'last_buy.html', context={'data': res})


def charts(request, data_id):
    res = get_charts(data_id)
    return render(request, 'charts.html', context={'data': res})


def stats(request, link):
    # return HttpResponse('/equities/' + link)
    res, naming = get_money('/equities/' + link)
    return render(request, 'stats.html', context={'data': res, 'naming': naming})


def acc_index(request):
    data = get_actions_online(short=True)
    valute = get_valute()
    return render(request, 'index.html', context={'data': data, 'valute': valute})


def acc_stock(request, data_id='', name='', link=''):
    if "name" in request.POST:
        mock = cache.get_or_set('mock', {})
        data = request.POST
        if not data["name"] in mock:
            mock[data["name"]] = {}
            mock[data["name"]]['money'] = 0.0
            mock[data["name"]]['amount'] = 0
        mock[data["name"]]['money'] += float(data["price"].replace('.', '').replace(',', '.'))
        mock[data["name"]]['amount'] += 1
        cache.set('mock', mock)
    if data_id == '':
        site = 'https://ru.investing.com/equities/most-active-stocks'
        res = get_actions_online(site)
        return render(request, 'last_buy.html', context={'data': res})
    data = get_charts(data_id)
    return render(request, 'stock.html', context={'data': data, 'name': name, 'link': link})


def acc_post(request):
    return render(request, 'post.html')


def portfolio(request):
    mock = cache.get_or_set('mock', {})
    # mock = {'Газпром': {'money': 100500, 'amount': 20}, 'rger': {'money': 100500, 'amount': 20}}
    data = []
    for x in mock.items():
        data.append({'name': x[0], 'money': round(x[1]['money'], 4), 'amount': x[1]['amount']})
    return render(request, 'portfolio.html', context={"data": data})


def send_mess(request):
    send_message()
    return HttpResponse('sent')
