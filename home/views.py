from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView
from django.views.generic import DetailView
from job.models import Job
from job.forms import Jobform,ApplyForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.


def home(request):
    # Fetch the job list
    job_list = Job.objects.all()  # You can customize this query based on your requirements
    paginator = Paginator( job_list, 2) 
    page_number = request.GET.get('page')
    job_list = paginator.get_page(page_number)
    # Pass the job list to the template
    context = {'job_list': job_list}
    return render(request, 'home/home.html', context)

class HomeJobListView(ListView):
    model = Job  # Use the Job model from the jobs app
    template_name = 'home/home_job_list.html'
    context_object_name = 'job_list'


class HomeJobDetailView(DetailView):
    model = Job
    template_name = 'home/home_job_details.html'  # Update this to your actual template path
    context_object_name = 'job'
    form_class = ApplyForm # Use the JobForm instead of creating a new form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()  # Instantiate the form
        return context
    
@login_required    
def home_post_job(request):
    if request.method == 'POST':
        form = Jobform(request.POST, request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()

            messages.success(request, 'Congratulations! The job has been successfully posted. We look forward to receiving qualified candidates!')
            request.session['show_message'] = True  # Set session variable
            return redirect('jobs:job_list')  # Redirect to the job list page or any other page you prefer
    else:
        form = Jobform()

    context = {
        'form1': form
    }

    request.session.pop('show_message', None)
    return render(request, 'home/home_post_job.html', context)