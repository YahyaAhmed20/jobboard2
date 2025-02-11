from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey('City', related_name='user_city', on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='profile/')
    cv = models.FileField(
        upload_to='applications/cvs/',
        verbose_name="CV/Resume",
        help_text="Upload your CV or resume in PDF or DOCX format.",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])],
        blank=True,  # Allow blank values in forms
        null=True    # Allow null values in the database
    )
    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)      
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class City(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
           return (self.name)
       
def clean(self):
        """
        Custom validation for the model.
        """
        super().clean()
        if not self.cv:
            raise ValueError("A CV or resume must be uploaded.")
