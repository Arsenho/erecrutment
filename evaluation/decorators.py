from functools import wraps
import datetime

from rest_framework.response import Response
from rest_framework import status

from evaluation.models import Solution, Test, Evaluation
from evaluation.serializers import SolutionSerializer, EvaluationSerializer, \
    TestSerializer
from joboffer.models import Offer, TestForOffer
from joboffer.serializers import OfferSerializer, TestForOfferSerializer


def save_question_answer(view_function):
    @wraps(view_function)
    def wrapped(self, request, *args, **kwargs):
        try:
            question_answer = Solution.objects.get(pk=int(request.data['answer']))
            question_answer_serializer = SolutionSerializer(question_answer, many=False)
            if int(request.data['question']) == question_answer_serializer.data['question']:
                print(question_answer_serializer.data)
                kwargs['ok'] = True
            else:
                kwargs['question_incompatibility'] = True
        except Solution.DoesNotExist:
            pass
        except TypeError:
            kwargs['conversion_error'] = True
        except ValueError:
            kwargs['conversion_error'] = True
        return view_function(self, request, *args, **kwargs)

    return wrapped


def is_applicant(view_function):
    @wraps(view_function)
    def wrapped(self, request, *args, **kwargs):
        if 'offer_id' in request.session:
            offer = Offer.objects.get(pk=int(request.session['offer_id']))
            offer_applicants = offer.applicants.all()
            if kwargs['candidate'] in offer_applicants:
                today = datetime.date.today()
                if today > offer.ends:
                    return Response(
                        data={'message': "Dsl la date limite est depassee !!!"},
                        status=status.HTTP_200_OK
                    )
                return view_function(self, request, *args, **kwargs)
            else:
                return Response(
                    data={
                        'message': "veuillez postuler d'abord a l'offre",
                        'participant': False
                    },
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                data={'message': "offre introuvable !!!"},
                status=status.HTTP_200_OK
            )

    return wrapped


def get_tests_for_offer(request):
    if 'offer_id' in request.GET:
        offer_id = int(request.GET['offer_id'])
        request.session['offer_id'] = offer_id
    try:
        offer = Offer.objects.get(pk=offer_id)
        offers_tests = TestForOffer.objects.filter(offer=offer)
        offers_tests_serializer = TestForOfferSerializer(offers_tests, many=True)
        tests = []

        for line in offers_tests_serializer.data:
            test_id = int(line['test'])
            test_priority = int(line['priority'])
            try:
                test = {
                    'test': TestSerializer(
                        Test.objects.get(pk=test_id),
                        many=False
                    ).data,
                    'priority': test_priority
                }
                tests.append(test)
            except Test.DoesNotExist:
                print("le test n'existe pas")
    except Offer.DoesNotExist:
        return Response(
            data={'message': "Cette offre n'existe pas !!!"},
            status=status.HTTP_404_NOT_FOUND
        )
    return tests


def can_take_evaluation(view_function):
    @wraps(view_function)
    def _wrapped(self, request, *args, **kwargs):
        tests = get_tests_for_offer(request=request)
        try:
            test_for_offer = TestForOffer.objects.filter()
            candidate_evaluation = Evaluation.objects.filter(candidate=kwargs['candidate'])

            if candidate_evaluation:
                return Response(
                    data={'take_evaluation': True},
                    status=status.HTTP_200_OK
                )
            else:
                request.session['tests'] = sorted(
                    tests,
                    key=lambda test_pri: test_pri['priority'],
                    reverse=True
                )
                kwargs['take_evaluation'] = False
                return view_function(self, request, *args, **kwargs)

        except Evaluation.DoesNotExist:
            return Response(
                data={'take_evaluation': False},
                status=status.HTTP_200_OK
            )

    return _wrapped
