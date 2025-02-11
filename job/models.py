from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now
JOB_TYPE_CHOICES = [
    ('Full-Time', 'Full-Time'),
    ('Part-Time', 'Part-Time'),
    ('Internship', 'Internship'),
    ('Contract', 'Contract'),
    ('Freelance', 'Freelance'),
]

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Any', 'Any'),  # Added 'Any' as an option
]

STATUS_CHOICES = [
    ('Active', 'Active'),
    ('Closed', 'Closed'),
    ('Draft', 'Draft'),
]

def upload_to(instance, filename):
    return f"job_images/{instance.slug}/{filename}"

def generate_unique_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug}-{get_random_string(length=4)}"
        return generate_unique_slug(instance, new_slug=new_slug)
    return slug

class Job(models.Model):
    owner = models.ForeignKey(User, related_name='job_owner', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True, help_text="Enter the job title")
    description = models.TextField(help_text="Provide a detailed description of the job")
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default='Full-Time',
        help_text="Select the type of job"
    )
    image = models.ImageField(upload_to=upload_to, blank=True, null=True, help_text="Upload a relevant image")
    location = models.CharField(max_length=200, db_index=True, help_text="Enter the job location")
    vacancy = models.PositiveIntegerField(default=1, help_text="Enter the number of vacancies")
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Enter the salary range (optional)"
    )
    responsibilities = models.TextField(help_text="List the job responsibilities")
    qualifications = models.TextField(help_text="List the required qualifications")
    benefits = models.TextField(help_text="List the job benefits")
    published_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category',on_delete=models.CASCADE)
    experience = models.CharField(max_length=200, help_text="Enter the required experience level")
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='Any',
        help_text="Select the preferred gender (if applicable)"
    )
    slug = models.SlugField(unique=True, blank=True, help_text="Auto-generated slug for URLs")
    application_deadline = models.DateTimeField(blank=True, null=True, help_text="Set the application deadline")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Draft',
        help_text="Select the job status"
    )
    
   
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"
    

class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Order categories alphabetically by name
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        permissions = [
            ("can_view_all_jobs", "Can view all job listings"),
            ("can_edit_job", "Can edit job listings"),
        ]
        
        


class Apply(models.Model):
    """
    Model representing a job application submitted by a candidate.
    """

    # Fields
    job = models.ForeignKey(
        Job,
        related_name='applications',
        on_delete=models.CASCADE,
        verbose_name="Job Applied For",
        help_text="The job this application is for."
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Full Name",
        help_text="The full name of the applicant."
    )
    email = models.EmailField(
        max_length=100,
        verbose_name="Email Address",
        help_text="The email address of the applicant."
    )
    website = models.URLField(
        null=True,
        blank=True,
        verbose_name="Personal Website",
        help_text="Optional: The applicant's personal or portfolio website."
    )
    cv = models.FileField(
        upload_to='applications/cvs/',
        verbose_name="CV/Resume",
        help_text="Upload your CV or resume in PDF or DOCX format.",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])]
    )
    cover_letter = models.TextField(
        max_length=500,
        verbose_name="Cover Letter",
        help_text="A brief introduction and why you're a good fit for the job."
    )
    created_at = models.DateTimeField(
        default=now,
        editable=False,
        verbose_name="Application Date",
        help_text="The date and time when the application was submitted."
    )

    # Metadata
    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"
        ordering = ['-created_at']  # Newest applications first

    # Methods
    def __str__(self):
        """
        Returns a string representation of the application.
        """
        return f"{self.name} - {self.job.title}"

    def clean(self):
        """
        Custom validation for the model.
        """
        super().clean()
        if not self.cv:
            raise ValueError("A CV or resume must be uploaded.")
