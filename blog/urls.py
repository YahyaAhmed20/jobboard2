from django.urls import path,include
from . import views

app_name='blog'
urlpatterns = [
    path('', views.blog, name='blog'),  # URL for the job list view
  
]