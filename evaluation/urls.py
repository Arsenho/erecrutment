from django.urls.conf import path
from django.conf.urls import url

from evaluation.views import QuestionList, SolutionList, EvaluationList, \
    TestList, ParticipateList, TakeEvaluation, TestDetail, ParticipateDetail

urlpatterns = [
    url(r'^api/questions/$', view=QuestionList.as_view(), name='questions'),
    url(r'^api/solutions/$', view=SolutionList.as_view(), name='solutions'),
    url(r'^api/evaluations/$', view=EvaluationList.as_view(), name='evaluations'),
    url(r'^api/tests/$', view=TestList.as_view(), name='tests'),
    path('api/tests/<int:pk>/', view=TestDetail.as_view(), name='tests_'),
    url(r'^api/take/$', view=TakeEvaluation.as_view(), name='take'),
    url(r'^api/participates/$', view=ParticipateList.as_view(), name='participates'),
    path('api/participates/<int:pk>', view=ParticipateDetail.as_view(), name='participates_update'),
]
