from rest_framework import serializers

from registration.serializers import CandidateSerializer
from .models import Offer, Apply


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
