from rest_framework import serializers

from registration.serializers import CandidateSerializer
from .models import *


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class ParticipateSerializer(serializers.ModelSerializer):
    test = TestSerializer()
    candidate = CandidateSerializer()

    class Meta:
        model = Participate
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'