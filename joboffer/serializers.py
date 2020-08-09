from rest_framework import serializers

from registration.serializers import CandidateSerializer, EmployerSerializer
from .models import Offer, Apply, Company, Attachment, TestForOffer, EvaluationForOffer


class CompanySerializer(serializers.ModelSerializer):
    # created_by = EmployerSerializer()

    class Meta:
        model = Company
        exclude = [
            'created',
            'modified',
        ]
        extra_kwargs = {
            'created_by': {'read_only': True},
        }


class OfferSerializer(serializers.ModelSerializer):
    # company = CompanySerializer()

    class Meta:
        model = Offer
        exclude = [
            'created',
            'modified',
        ]
        extra_kwargs = {
            'published_by': {'read_only': True},
        }


class TestForOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestForOffer
        fields = '__all__'
        extra_kwargs = {}


class EvalForOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationForOffer
        exclude = ['created']
        extra_kwargs = {}


class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        exclude = [
            'created',
            'modified',
            'candidate',
        ]
        extra_kwargs = {
        }


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        exclude = [
            'created',
            'modified',
        ]


class OfferCategory(serializers.Serializer):
    category = serializers.CharField(max_length=128)
