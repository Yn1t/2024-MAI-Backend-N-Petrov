from django.urls import path
from . import views

urlpatterns = [
    path('customers', views.all_customers, name='customers'),
    path('customers/<slug:customer_id>', views.customer, name='customer'),
    path('customer_create', views.create_customer, name='customer_create'),

    path('dishes/<slug:customer_id>', views.all_customer_dishes, name='dishes'),
    path('dish_create', views.create_dish, name='dish_create'),
    path('dish_search', views.search_dish, name='search_dish'),

    path('menu/<slug:menu_name>', views.menu, name='menu'),
    path('menu', views.all_menu, name='all_menu'),
    path('menu_create', views.create_menu, name='menu_create'),
]
