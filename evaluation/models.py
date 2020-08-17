import datetime

from django.db import models
from registration.models import Employer, Candidate, User


# Create your models here.


class Test(models.Model):
    TEST_TYPES = [
        ('psychotechnique', 'Psychotechnique'),
        ('personnalite', 'Personnalite'),
        ('comportement_professionnel', 'Comportement professionnel'),
        ('motivation', 'Motivation'),
        ('test_de_raisonnement_R', 'Test de raisonnement R'),
    ]
    title = models.CharField(max_length=128, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    initial = models.BooleanField(default=False)
    type_of_test = models.CharField(
        max_length=128, null=True,
        blank=True, choices=TEST_TYPES
    )
    created_by = models.ForeignKey(
        User,  # the user must be either an employer or the superuser
        on_delete=models.CASCADE,
        null=True,
        related_name="user_who_created_the_test"
    )
    questions = models.ManyToManyField(
        "Question",
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    participants = models.ManyToManyField(
        Candidate,
        blank=True,
        through="Participate",
        related_name="candidate_who_participate_to_a_test"
    )

    def __str__(self):
        return self.title

    def set_participants(self):
        participates = Participate.objects.filter(test=self.pk)
        candidates = []
        for participate in participates:
            if datetime.date.today() > participate.evaluation_date:
                candidate = Candidate.objects.get(id=participate.candidate.pk)
                candidates.append(candidate)
        self.participants.set(candidates)


class Participate(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)
    evaluation_date = models.DateField(blank=True, null=True)
    score = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    text = models.TextField(null=True, blank=True, unique=True)
    question_type = models.CharField(max_length=128, blank=True, null=True)
    created_by = models.ForeignKey(
        User,  # the user can either be an Employer or the superuser
        on_delete=models.CASCADE, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    being_answered_by = models.ManyToManyField(
        Candidate,
        blank=True,
        related_name="candidate_answering_question",
        through="Evaluation"
    )

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.text


class Solution(models.Model):
    text = models.TextField(null=True, unique=True, blank=True)
    created_by = models.ForeignKey(
        User,  # the user must be either the superuser or an employer
        on_delete=models.CASCADE, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.pk) + " -> " + str(self.text)


class Evaluation(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name="candidate_who_answered_question"
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name="test_for_current_evaluation"
    )
    created = models.DateTimeField(auto_now_add=True)
    answer = models.ForeignKey(
        Solution,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
