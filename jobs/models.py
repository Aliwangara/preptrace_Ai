from django.db import models
from django.conf import settings

# Create your models here.
class Job(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobs",
        
    )
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    link = models.URLField()
    site = models.CharField(max_length=100, default="Unknown")  
    tech_stack = models.CharField(max_length=500, blank=True, null=True)
    logo = models.URLField(blank=True, null=True)   
              

    def __str__(self):
        return f"{self.title} at {self.company} ({self.site})"


