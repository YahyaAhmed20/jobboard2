
from django.shortcuts import render,get_object_or_404,redirect
from .models import Job
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .filters import JobFilter
from .forms import ApplyForm,Jobform
# Create your views here.

def job_list(request):
    # Return all job 
    job_list = Job.objects.all()
    myfilter = JobFilter(request.GET, queryset=job_list)
    job_list = myfilter.qs

    

    paginator = Paginator(job_list, 2)
    page_number = request.GET.get('page')
    job_list = paginator.get_page(page_number)

    context = {'job_list': job_list,'myfilter': myfilter} # Define context outside the else block
    return render(request, 'job/job_list.html', context)


def job_detail(request, slug):
    # Fetch the job detail using the slug
    job_detail = get_object_or_404(Job, slug=slug)

    # Initialize the form outside the POST block
    form = ApplyForm()

    if request.method == 'POST':
        # Process the form data if the request method is POST
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.job = job_detail  # Associate the form with the current job
            myform.save()  # Save the form data to the database
            return redirect('jobs:job_list')

    # Pass the form and job detail to the template
    context = {'job_detail': job_detail, 'form': form}

    return render(request, 'job/job_detail.html', context)



@login_required  # Add this decorator to enforce login requirement
def add_job(request):
    if request.method == 'POST':
        form1 = Jobform(request.POST, request.FILES)
        if form1.is_valid():
            myform = form1.save(commit=False)
            myform.owner = request.user  # Assign the current user as the owner
            myform.save()
            return redirect('jobs:job_list')  # Redirect to job list after saving
    else:
        form1 = Jobform()  # Initialize an empty form for GET requests

    context = {
        'form1': form1,
    }

    return render(request, 'job/add_job.html', context)


