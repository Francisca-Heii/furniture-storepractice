
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.views_bag, name='views_bag'),
    path('add/<item_id>', views.add_to_bag, name='add_to_bag'),
    path('adjust/<item_id>', views.add_to_bag, name='adjust_bag'),
    path('remove/<item_id>', views.remove_from_bag, name='remove_from_bag'),

    
]
