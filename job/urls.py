from django.urls import path,include
from . import views

app_name='job'
urlpatterns = [
    path('', views.job_list, name='job_list'),  # URL for the job list view
    path('<int:id>/', views.job_detail, name='job_detail'),  # URL for the job detail view
]
