from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from .managers import CustomUserManager
from django.conf import settings


# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    tech_stack = models.CharField(max_length=100,blank=True)
    cv = models.FileField(upload_to='accounts/cvs',blank=True,null=True)
    ats_score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.email}'s profile"
    

class JobApplication(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30,
        choices=[
            ('pending', 'Pending'),
            ('applied', 'Applied'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} -> {self.job.title} ({self.status})"
    
