from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .actions import *


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
