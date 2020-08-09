import datetime
import random

from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

# imports from current app
from erecrutment.decorators import login_required_for_candidate, \
    login_required_for_employer
from evaluation.decorators import save_question_answer, is_applicant, can_take_evaluation
from evaluation.models import Question, Solution, Test, \
    Participate, Evaluation
from evaluation.serializers import QuestionSerializer, SolutionSerializer, \
    EvaluationSerializer, TestSerializer, ParticipateSerializer
from joboffer.models import Offer, TestForOffer, EvaluationForOffer
from joboffer.serializers import TestForOfferSerializer, EvalForOfferSerializer
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


def set_participants(test):
    print('setting participants')
    participates = Participate.objects.filter(test=test.pk)
    test_for_offer = TestForOffer.objects.filter(test=test.pk)
    test_for_offer_serializer = TestForOfferSerializer(test_for_offer, many=True)
    print(test_for_offer_serializer.data)
    candidates = []
    for participate in participates:
        today = datetime.date.today()
        if today >= participate.evaluation_date:
            print('got a participant')
            candidate = Candidate.objects.get(id=participate.candidate.pk)
            candidates.append(candidate.pk)
    return candidates


class TestList(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        tests = []
        for test in serializer.data:
            test_ = Test.objects.get(id=test.get('id'))
            data = TestSerializer(test_).data
            data['participants'] = set_participants(test_)
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


class TestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response()


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


class ParticipateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Participate.objects.all()
    serializer_class = ParticipateSerializer


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


def get_generated_list(test):
    # test_serializer = TestSerializer(Test.objects.get(id=test_id))
    questions = list(test['questions'])
    generate = question_generator(questions)
    questions_list = [next(generate) for i in range(len(questions))]
    question_id = questions_list.pop()
    question = QuestionSerializer(
        Question.objects.get(id=question_id)
    )
    return question, questions_list


def save_evaluation_for_offer(request, evaluation):
    if 'offer' in request.session:
        offer = request.session['offer']
        data = {
            'offer': offer['id'],
            'evaluation': evaluation['id']
        }
        eval_for_offer = EvalForOfferSerializer(data=data, many=False)
        if eval_for_offer.is_valid():
            eval_for_offer.save()
        else:
            print("Erreur lors de la sauvegarde Eval for offer")
        return True
    return False


class TakeEvaluation(generics.ListCreateAPIView):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer

    @login_required_for_candidate
    @is_applicant
    @can_take_evaluation
    def get(self, request, *args, **kwargs):
        question = None

        if 'QUESTIONS_IDS' in request.session:
            del request.session['QUESTIONS_IDS']

        if 'tests' in request.session and \
                (request.session['tests'] != []):
            if 'QUESTIONS_IDS' not in request.session:
                tests = list(request.session['tests'])
                test = tests.pop(-1)
                request.session['tests'] = tests
                generate = get_generated_list(test['test'])
                question = generate[0]
                request.session['QUESTIONS_IDS'] = generate[1]
            return Response(
                data=question.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={'message': "Aucun test n'est associee a cette offre"},
                status=status.HTTP_200_OK
            )

    @login_required_for_candidate
    @is_applicant
    @save_question_answer
    def post(self, request, *args, **kwargs):
        question = None
        if 'ok' in kwargs and kwargs['ok']:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['candidate'] = kwargs['candidate']
            self.perform_create(serializer)
            save_evaluation_for_offer(request, evaluation=serializer.data)

        if 'tests' in request.session and \
                (request.session['tests'] != []):
            if 'QUESTIONS_IDS' not in request.session:
                tests = list(request.session['tests'])
                test = tests.pop(-1)
                request.session['tests'] = tests
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
                        data={'message': 'test termine !', 'finish': True},
                        status=status.HTTP_200_OK
                    )
                if 'tests' in request.session:
                    generate = get_generated_list(test['test'])
                    question = generate[0]
                    request.session['QUESTIONS_IDS'] = generate[1]

            return Response(
                data=question.data,
                status=status.HTTP_200_OK
            )
        else:
            if 'QUESTIONS_IDS' in request.session and \
                    (request.session['QUESTIONS_IDS'] != []):
                updates = update_questions_id(list(request.session['QUESTIONS_IDS']))
                question = updates[1]
                request.session['QUESTIONS_IDS'] = updates[0]
                return Response(
                    data=question.data,
                    status=status.HTTP_200_OK
                )

            del request.session['tests']
            return Response(
                data={'message': 'tous les tests termines !', 'finish': True},
                status=status.HTTP_200_OK
            )
