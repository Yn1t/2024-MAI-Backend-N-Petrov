from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.forms import model_to_dict

import json

from .models import Customer, Dish, Menu


# Create your views here.


@csrf_exempt
@require_http_methods(["GET"])
def customer(request, customer_id):
    customer_ = Customer.objects.get(login=customer_id)
    context = {'customer': model_to_dict(customer_)}
    return JsonResponse(context)


@csrf_exempt
@require_http_methods(["GET"])
def menu(request, menu_name):
    menu_ = Menu.objects.get(name=menu_name)
    return JsonResponse(list(menu_.dishes.values()),
                        safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@require_http_methods(["GET"])
def all_customers(request):
    return JsonResponse(list(Customer.objects.all().values()),
                        safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@require_http_methods(["GET"])
def all_customer_dishes(request, customer_id):
    customer_ = Customer.objects.get(login=customer_id)
    return JsonResponse(list(Dish.objects.filter(customer_id=customer_).values()),
                        safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@require_http_methods(["GET"])
def all_menu(request):
    return JsonResponse(list(Menu.objects.all().values()),
                        safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@require_http_methods(["POST"])
def create_customer(request):
    post_data = json.loads(request.body.decode("utf-8"))
    Customer.objects.create(login=post_data['login'], password=post_data['password'])
    return JsonResponse({'status': 'ok'})


@csrf_exempt
@require_http_methods(["POST"])
def create_dish(request):
    post_data = json.loads(request.body.decode("utf-8"))
    if "customer" in post_data:
        Dish.objects.create(type=post_data['type'], name=post_data['name'],
                            weight=post_data['weight'],
                            customer_id=Customer.objects.get(login=post_data["customer"]),
                            for_menu=False)
    else:
        if not Dish.objects.filter(name=post_data['name'], for_menu=True).exists():
            Dish.objects.create(type=post_data['type'], name=post_data['name'],
                                weight=post_data['weight'])

    return JsonResponse({'status': 'ok'})


@csrf_exempt
@require_http_methods(["POST"])
def create_menu(request):
    data = json.loads(request.body.decode("utf-8"))
    new_menu = Menu.objects.create(type=data['type'], name=data['name'])
    for dish_data in data["dishes"]:
        dish = Dish.objects.get(name=dish_data, for_menu=True)
        new_menu.dishes.add(dish)
    return JsonResponse({'status': 'ok'})


@csrf_exempt
@require_http_methods(["GET"])
def search_dish(request):
    query = request.GET.get('q', '')
    dishes = Dish.objects.filter(name__icontains=query, for_menu=True) | \
             Dish.objects.filter(type__icontains=query, for_menu=True)
    if dishes:
        return JsonResponse(list(dishes.values()),
                            safe=False, json_dumps_params={'ensure_ascii': False})

    return JsonResponse({[]})
