from django.shortcuts import render,redirect
from django.conf import settings
from .models import Info
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib import messages

# Create your views here.


def send_text(request):
    myinfo = Info.objects.first()
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        sender_email = request.POST['email']  # Get sender's email from the form
        recipient_email = settings.EMAIL_HOST_USER  # Your email address
        

        # Send the email
        send_mail(
            subject,
            f"Sender's Email: {sender_email}\n\n{message}",
            recipient_email,  # Use your email address as the recipient
            [sender_email],  # Use the sender's email address as the recipient
            fail_silently=False,
        )
        #redirect 
        messages.success(request, 'Your message has been sent successfully!')
        request.session['show_message'] = True
        return redirect('jobs:job_list')

                   
    return render(request,'contact/contactus.html',{'myinfo':myinfo})