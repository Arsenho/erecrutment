from django.urls.conf import path
from django.conf.urls import url

from evaluation.views import QuestionList, SolutionList, EvaluationList, TestList, ParticipateList, TakeEvaluation

urlpatterns = [
    url(r'^api/questions/', view=QuestionList.as_view(), name='questions'),
    url(r'^api/solutions/', view=SolutionList.as_view(), name='solutions'),
    url(r'^api/evaluations/', view=EvaluationList.as_view(), name='evaluations'),
    url(r'^api/tests/', view=TestList.as_view(), name='tests'),
    url(r'^api/take/', view=TakeEvaluation.as_view(), name='take'),
    url(r'^api/participates/', view=ParticipateList.as_view(), name='participates'),
]
