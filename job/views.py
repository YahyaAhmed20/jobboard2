from django.shortcuts import render
from .models import Job
# Create your views here.

def job_list(request):
    # Return all job 
    job_list = Job.objects.all()
    context = {'job_list': job_list} # Define context outside the else block
    return render(request, 'job/job_list.html', context)


def job_detail(request,id):
        # Return all job with ID
    job_detail = Job.objects.get(id=id)
    context = {'job_detail': job_detail}  # Define context outside the else block
    return render(request, 'job/job_detail.html', context)

