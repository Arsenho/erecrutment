from rest_framework import serializers

from registration.serializers import CandidateSerializer
from .models import *


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True},
            'created': {'read_only': True},
            'modified': {'read_only': True},
        }


class ParticipateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participate
        fields = '__all__'
        extra_kwargs = {
            'candidate': {'read_only': True},
            'score': {'read_only': True},
        }


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = [
            'created',
            'modified',
        ]
        extra_kwargs = {
            'created_by': {'read_only': True}
        }


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        exclude = [
            'created',
            'modified',
        ]
        extra_kwargs = {
            'created_by': {'read_only': True}
        }


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'
        extra_kwargs = {
            'candidate': {'read_only': True},
            'created': {'read_only': True},
        }
