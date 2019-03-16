from django.contrib import admin
from .views import *
from django.urls import path

urlpatterns = [
    path('',post_list,name='post_list'),
    path('delete/<slug:slug>/',post_delete,name='post_delete'),
    path('detail/<slug:slug>/',post_detail,name='post_detail'),
    path('update/<slug:slug>/',post_update,name='post_update'),
    path('create/',post_create,name='post_create'),
]