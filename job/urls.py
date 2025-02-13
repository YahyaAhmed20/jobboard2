from django.urls import path, include
from . import views
from . import api

app_name = 'job'
urlpatterns = [
    path('', views.job_list, name='job_list'),  # URL for the job list view
    path('add/', views.add_job, name='add_job'),
    path('<str:slug>/', views.job_detail, name='job_detail'),  # URL for the job detail view
    
    # API 
    path('api/v2/jobs', api.JobListApi.as_view(), name='JobListApi'),
    path('api/V2/jobs/<int:id>', api.JobDetail.as_view(), name='JobDetail'),
]