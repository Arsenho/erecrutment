from django.db import models

# Create your models here.
from registration.models import Employer, Candidate


class Test(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    typeOfTest = models.CharField(max_length=128, null=True, blank=True)
    created_by = models.ForeignKey(Employer, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField("Question")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    participants = models.ManyToManyField(Candidate, blank=True, through="Participate")

    def __str__(self):
        return self.title


class Participate(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)
    score = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    text = models.TextField(null=True, blank=True, unique=True)
    created_by = models.ForeignKey(Employer, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)


class Solution(models.Model):
    text = models.TextField(null=True, unique=True, blank=True)
    created_by = models.ForeignKey(Employer, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
