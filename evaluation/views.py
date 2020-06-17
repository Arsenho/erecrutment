import datetime
import random

from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

# imports from current app
from erecrutment.decorators import login_required_for_candidate, login_required_for_employer
from evaluation.models import Question, Solution, Evaluation, Test, Participate
from evaluation.serializers import QuestionSerializer, SolutionSerializer, EvaluationSerializer, TestSerializer, \
    ParticipateSerializer
from registration.models import Candidate
from registration.serializers import CandidateSerializer


class QuestionList(generics.ListCreateAPIView):
    """
    allows get and post methods,
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, *args, **kwargs):
        # this list will contain the new question structure that
        # would be return to the user
        data = []

        queryset = self.filter_queryset(self.get_queryset())
        question_serializer = self.get_serializer(queryset, many=True)

        # get all solutions related to a question
        # a question value a tuple type. e.g fir id field we have ('id', 1)
        for question in question_serializer.data:
            solutions = Solution.objects.filter(question=question.get('id'))
            solution_serializer = SolutionSerializer(solutions, many=True)
            my_data = {
                'question': question,
                'solutions': solution_serializer.data
            }
            data.append(my_data)
        return Response(data=data, status=status.HTTP_200_OK)

    @login_required_for_employer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['created_by'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class SolutionList(generics.ListCreateAPIView):
    """
    allows get and post methods,
    """

    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer

    @login_required_for_employer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['created_by'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class EvaluationList(generics.ListCreateAPIView):
    """
    allows get and post methods,
    """

    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

    @login_required_for_candidate
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['candidate'] = kwargs['candidate']
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class TestList(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def set_participants(self, test):
        participates = Participate.objects.filter(test=test.pk)
        candidates = []
        for participate in participates:
            today = datetime.date.today()
            if today > participate.evaluation_date:
                candidate = Candidate.objects.get(id=participate.candidate.pk)
                candidates.append(candidate.pk)
        return candidates

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        tests = []
        for test in serializer.data:
            test_ = Test.objects.get(id=test.get('id'))
            data = TestSerializer(test_).data
            data['participants'] = self.set_participants(test_)
            tests.append(data)
        return Response(data=tests, status=status.HTTP_200_OK)

    @login_required_for_employer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['created_by'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ParticipateList(generics.ListCreateAPIView):
    queryset = Participate.objects.all()
    serializer_class = ParticipateSerializer

    @login_required_for_candidate
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['candidate'] = kwargs['candidate']
        test_serializer = TestSerializer(
            serializer.validated_data['test']
        )
        if test_serializer.data['initial']:
            serializer.validated_data['evaluation_date'] = datetime.date.today()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


def question_generator(ids: list):
    """
    Receive a list of question ids coming from a test associated to an offer
    and return the next random question is
    :param ids:
    :return: int
    """
    while ids:
        question_id = random.choice(ids)
        yield question_id
        ids.remove(question_id)
    return 0


def update_questions_id(questions_ids):
    questions_list_ = list(questions_ids)
    question_id_ = questions_list_.pop()
    question_ = QuestionSerializer(
        Question.objects.get(id=question_id_)
    )
    return questions_list_, question_


def get_generated_list(test_id):
    test_serializer = TestSerializer(Test.objects.get(id=test_id))
    questions = list(test_serializer.data['questions'])
    generate = question_generator(questions)
    questions_list = [next(generate) for i in range(len(questions))]
    question_id = questions_list.pop()
    question = QuestionSerializer(
        Question.objects.get(id=question_id)
    )
    return question, questions_list


class TakeEvaluation(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def post(self, request, *args, **kwargs):
        if 'QUESTIONS_IDS' in request.session and \
                (request.session['QUESTIONS_IDS'] != []):
            updates = update_questions_id(list(request.session['QUESTIONS_IDS']))
            question = updates[1]
            request.session['QUESTIONS_IDS'] = updates[0]
        else:
            if 'QUESTIONS_IDS' in request.session and \
                    (request.session['QUESTIONS_IDS'] == []):
                del request.session['QUESTIONS_IDS']
                return Response(
                    data={'message': 'test termine !'},
                    status=status.HTTP_200_OK
                )
            generate = get_generated_list(2)
            question = generate[0]
            request.session['QUESTIONS_IDS'] = generate[1]

        return Response(
            data=question.data,
            status=status.HTTP_200_OK
        )
