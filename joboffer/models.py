from django.db import models
from evaluation.models import Test
from registration.models import Employer, Candidate


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=128, blank=True)
    company_type = models.CharField(max_length=128, blank=True, null=True)
    company_domain = models.CharField(max_length=256, blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    site = models.CharField(max_length=128, blank=True, null=True)
    location = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)


class Offer(models.Model):
    OFFER_TYPES = [
        ('emploi', 'Emploi'),
        ('stage', 'stage'),
    ]
    EXPERIENCES = [
        ('', '0-1'),
        ('', '1-3'),
        ('', '3-5'),
        ('', '5-7'),
    ]
    title = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        unique=True
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    level = models.CharField(max_length=128, blank=True, null=True)
    contract_type = models.CharField(max_length=128, blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    post = models.CharField(max_length=128, blank=True)
    offer_type = models.CharField(
        choices=OFFER_TYPES,
        null=True,
        blank=True,
        max_length=32
    )
    competence = models.CharField(max_length=128, null=True)
    experience = models.CharField(max_length=32, null=True)
    begins = models.DateField(null=True, blank=True)
    ends = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    published_by = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE,
        related_name="employer_created_offer",
        null=True
    )
    description = models.TextField(null=True, blank=True)
    tests = models.ManyToManyField(Test, blank=True)
    applicants = models.ManyToManyField(
        Candidate,
        related_name="candidates_applying_for_offer",
        through="Apply"
    )

    def __str__(self):
        return self.title


class Apply(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    cv = models.FileField(upload_to='candidates/cvs')
    created = models.DateTimeField(auto_now_add=True)


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/%Y/%M/%D/')
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        blank=True
    )
