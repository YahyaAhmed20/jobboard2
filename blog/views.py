from django.shortcuts import render
from django.shortcuts import render
from .models import BlogPost
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def blog(request):
    
       # Retrieve all posts and order them by created_at descending
    posts = BlogPost.objects.all().order_by('-created_at')
    
    # Create a Paginator object with 5 posts per page
    paginator = Paginator(posts, 1)  # Show 5 blog posts per page

    page = request.GET.get('page')  # Get the page number from the query string
    try:
        posts = paginator.page(page)  # Get the posts for the requested page
    except PageNotAnInteger:
        # If the page is not an integer, return the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, return the last page
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/blog.html',{'posts': posts,'paginator': paginator})