from django.urls import path, re_path
from django.contrib import admin

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
)

app_name = 'posts'

urlpatterns = [
    path('', post_list, name='list'),
    path('create/', post_create,name='create'),
    re_path(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    # path('posts/', "<appname>.views.<function_name>"),  # Left commented as it’s a placeholder
]