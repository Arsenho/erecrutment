from django.db import models
from registration.models import User, Employer


# Create your models here.
class Notification(models.Model):
    text = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, blank=True)
    created_by = models.ForeignKey(Employer, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
