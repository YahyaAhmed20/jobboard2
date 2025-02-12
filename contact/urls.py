from django.urls import path,include
from . import views

app_name='contact'
urlpatterns = [
    path('', views.send_text, name='send_text'),  # URL for the job list view
  
]
