from django.db import models
from evaluation.models import Test
from registration.models import Employer, Candidate


# Create your models here.
class Offer(models):
    OFFER_TYPES = [
        ('emploi', 'Emploi'),
        ('stage', 'stage'),
    ]
    title = models.CharField(max_length=128, null=True, blank=True, unique=True)
    offer_type = models.CharField(choices=OFFER_TYPES, null=True, blank=True, max_length=32)
    begins = models.DateField(null=True, blank=True)
    ends = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    published_by = models.ForeignKey(Employer, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True, blank=True)
    tests = models.ManyToManyField(Test, blank=True)
    applicants = models.ManyToManyField(Candidate, through="Apply")

    def __str__(self):
        return self.title


class Apply(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    cv = models.FileField(upload_to='candidates/cvs')
    created = models.DateTimeField(auto_now_add=True)
