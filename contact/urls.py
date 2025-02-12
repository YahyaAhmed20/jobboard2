from django.urls import path,include
from . import views

app_name='contact'
urlpatterns = [
    path('', views.contactus, name='contact'),  # URL for the job list view
  
]
