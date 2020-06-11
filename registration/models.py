from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    GENDERS = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    phone_number = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDERS, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)


class Admin(User):
    class Meta:
        verbose_name = 'Administrateur'


class Employer(User):
    company_name = models.CharField(max_length=128, null=True, blank=True)
    website = models.CharField(max_length=128, null=True, blank=True)


class Candidate(User):
    class Meta:
        verbose_name = 'Candidate'
