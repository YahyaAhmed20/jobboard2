# home


from django.urls import path
from .views import HomeJobDetailView

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.HomeJobListView.as_view(), name='home_job_list'),
    path('jobs/<slug:slug>/', HomeJobDetailView.as_view(), name='home_job_details'),
    path('post-job/', views.home_post_job, name='home_post_job'),

    
]