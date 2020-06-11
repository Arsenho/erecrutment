from rest_framework import serializers

from registration.serializers import CandidateSerializer, EmployerSerializer
from .models import Offer, Apply, Company


class CompanySerializer(serializers.ModelSerializer):
    created_by = EmployerSerializer()

    class Meta:
        model = Company
        exclude = [
            'created',
            'modified',
        ]


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class ApplySerializer(serializers.ModelSerializer):
    offer = OfferSerializer()
    candidate = CandidateSerializer()

    class Meta:
        model = Apply
        fields = '__all__'
