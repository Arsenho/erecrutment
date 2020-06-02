from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    surename = models.CharField(max_length=128, null=True, blank=True)
    username = models.CharField(max_length=64, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=128, null=True, blank=True, unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Admin(User):
    super = models.BooleanField(default=False)


class Employer(User):
    company_name = models.CharField(max_length=128, null=True, blank=True)
    website = models.CharField(max_length=128, null=True, blank=True)


class Candidate(User):
    pass


class Group(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, through="Member")


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)