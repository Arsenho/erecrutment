from django.conf.urls import url
from django.urls.conf import path

from . import views

urlpatterns = [
    url(r'^api/dashboard/participants-for-offer$', view=views.ParticipantForOffer.as_view()),
    url(r'^api/dashboard/participants-for-test$', view=views.ParticipantForTest.as_view()),
    url(r'^api/dashboard/success-per-test$', view=views.NumSuccessPerTestForOffer.as_view()),
    url(r'^api/dashboard/failure-per-test$', view=views.NumFailurePerTestForOffer.as_view()),
    url(r'^api/dashboard/succeeded_all_tests', view=views.BestParticipantProfileForOffer.as_view()),
    url(r'^api/dashboard/appliance_per_date', view=views.NumParticipantPerPeriod.as_view()),
    url(r'^api/dashboard/candidates-per-test', view=views.NumParticipantPerTest.as_view()),
    url(r'^api/dashboard/participant-percentage-per-test', view=views.ParticipantPercentagePerTest.as_view()),
]
