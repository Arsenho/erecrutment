from django.contrib import admin

# Register your models here.
from joboffer.models import Offer, EvaluationForOffer

admin.site.register(Offer)
admin.site.register(EvaluationForOffer)