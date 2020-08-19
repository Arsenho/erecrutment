import datetime

from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from evaluation.serializers import TestSerializer, EvaluationSerializer, \
    SolutionSerializer
from evaluation.models import Solution, Test
from joboffer.models import Apply
from registration.models import Candidate
from registration.serializers import CandidateSerializer
from .decorators import *


def all_candidates_for_offer(offer):
    participants = offer.applicants.all()
    candidates = CandidateSerializer(participants, many=True)

    return candidates.data, len(candidates.data)


def all_tests_for_offer(offer):
    tests = offer.tests.all()

    return tests


def all_evaluations_for_offer(offer):
    evaluations = offer.evaluations.all()
    evaluations_serializer = EvaluationSerializer(evaluations, many=True)

    return evaluations_serializer.data


def candidates_from_evaluation(evaluations):
    candidate_list = []
    for evaluation in evaluations:
        if evaluation['candidate'] not in candidate_list:
            candidate_list.append(evaluation['candidate'])
    return candidate_list, len(candidate_list)


def candidate_participated_to_test(offer):
    tests = all_tests_for_offer(offer)
    candidates = []
    labels = []
    chartData = []
    for test in tests:
        labels.append(test.title)
        cpt = 0
        evaluations = offer.evaluations.filter(test=test.id)
        for evaluation in evaluations:
            current_data = {
                'test': test.id,
                'candidate': evaluation.candidate.username
            }
            if current_data not in candidates:
                cpt += 1
                candidates.append(current_data)
        chartData.append(cpt)
    return candidates, chartData, labels


def all_evaluations_for_test(offer):
    tests = all_tests_for_offer(offer)
    date_for_evaluations = []
    for test in tests:
        evaluations = offer.evaluations.filter(test=test.id)
        evaluations_serializer = EvaluationSerializer(evaluations, many=True)
        number_of_participants = candidates_from_evaluation(evaluations_serializer.data)[0]
        all_candidate_data = []
        for candidate_id in number_of_participants:
            candidate_evaluations = evaluations.filter(candidate=candidate_id)
            candidate_evaluations_serializer = EvaluationSerializer(candidate_evaluations, many=True)
            candidate_data = {
                'candidate': candidate_id,  # candidate id
                'evaluations': candidate_evaluations_serializer.data  # evaluations for this candidate
            }
            all_candidate_data.append(candidate_data)
        evaluations_serializer = EvaluationSerializer(evaluations, many=True)
        data = {
            'test': test.id,  # test id
            'evaluations': evaluations_serializer.data,  # evaluations concerning this test
            'evaluations_per_candidate': all_candidate_data
        }
        date_for_evaluations.append(data)

    return date_for_evaluations


def correction(evaluation):
    answer = Solution.objects.get(id=evaluation['answer'])
    if answer.correct:
        return True
    return False


def evaluation_corr_per_candidate(evaluations_per_candidate):
    evaluations_per_candidate_data = []
    for data in evaluations_per_candidate:
        evaluations = data['evaluations']
        correct_answer = 0
        evaluations_length = len(evaluations)
        for evaluation in evaluations:
            answer = correction(evaluation)
            if answer:
                correct_answer += 1
        current_data = {
            'candidate': data['candidate'],
            'evaluation_length': evaluations_length,
            'number_passed': correct_answer,
            'number_failed': evaluations_length - correct_answer,
            'passed_percentage': (correct_answer / evaluations_length) * 100,
            'failed_percentage': ((evaluations_length - correct_answer) / evaluations_length) * 100,
        }
        evaluations_per_candidate_data.append(current_data)
    return evaluations_per_candidate_data


def evaluation_correction(evaluations_for_test):
    corrections_data_for_evaluation = []
    for data in evaluations_for_test:
        evaluations_per_candidate = data['evaluations_per_candidate']
        current_data = {
            'test': data['test'],
            'correction_per_candidate': evaluation_corr_per_candidate(evaluations_per_candidate)
        }
        corrections_data_for_evaluation.append(current_data)
    return corrections_data_for_evaluation


def candidate_passed_test(corr_per_candidate):
    candidate_passed_test_data = []
    labels = []
    chartData = []
    for data in corr_per_candidate:
        correction_per_candidate = data['correction_per_candidate']
        candidate_passed_data = []
        for candidate_data in correction_per_candidate:
            current_data = {
                'candidate': candidate_data['candidate'],
            }
            if candidate_data['passed_percentage'] >= 50:
                current_data['passed_percentage'] = round(candidate_data['passed_percentage'], 2)
                candidate_passed_data.append(current_data)
        test = Test.objects.get(id=data['test'])
        current_test = {
            'test': test.id,
            'candidates_passed': candidate_passed_data,
            'candidate_passed_length': len(candidate_passed_data)
        }
        labels.append(test.title)
        chartData.append(len(candidate_passed_data))
        candidate_passed_test_data.append(current_test)
    return candidate_passed_test_data, labels, chartData


def candidate_failed_test(corr_per_candidate):
    candidate_failed_test_data = []
    labels = []
    chartData = []
    for data in corr_per_candidate:
        correction_per_candidate = data['correction_per_candidate']
        candidate_failed_data = []
        for candidate_data in correction_per_candidate:
            current_data = {
                'candidate': candidate_data['candidate'],
            }
            if candidate_data['passed_percentage'] < 50:
                current_data['failed_percentage'] = round(candidate_data['passed_percentage'], 2)
                candidate_failed_data.append(current_data)
        test = Test.objects.get(id=data['test'])
        current_test = {
            'test': test.id,
            'candidates_failed': candidate_failed_data,
            'candidate_failed_length': len(candidate_failed_data)
        }
        labels.append(test.title)
        chartData.append(len(candidate_failed_data))
        candidate_failed_test_data.append(current_test)
    return candidate_failed_test_data, labels, chartData


def candidate_passed_all_test(participants, candidate_passed_tests):
    candidate_passed_all_test_data = []
    for candidate in participants:
        cpt = 0
        total = 0
        for data in candidate_passed_tests:
            candidate_passed = data['candidates_passed']
            for passed in candidate_passed:
                if candidate == passed['candidate']:
                    cpt += 1
                    total += passed['passed_percentage']
                    print(total)
        if cpt == len(candidate_passed_tests):
            candidate = Candidate.objects.get(id=candidate)
            current_data = {
                'candidate': candidate.username,
                'total_percentage': round((total / len(candidate_passed_tests)), 2)
            }
            candidate_passed_all_test_data.append(current_data)
    return candidate_passed_all_test_data


def get_data(tests, evaluations_for_offer):
    data = []
    labels = []
    chartData = []
    number_of_participants = candidates_from_evaluation(evaluations_for_offer)[1]
    for test in tests:
        cpt = 0
        for evaluation in evaluations_for_offer:
            if evaluation['test'] == test.id:
                cpt += 1
        data_for_test = {
            'test': test.id,  # test id
            'number_of_question_answered_by_all_candidates': cpt,  # Nombre de candidat ayant pris part a ce test
            'number_of_participants': number_of_participants
        }
        labels.append(test.title)
        chartData.append(cpt)
        data.append(data_for_test)

    return data, labels, chartData


def get_applicants_per_period(appliances):
    apply_dates = []
    candidates_per_apply_dates = []
    for application in appliances:
        apply_date = datetime.datetime.date(application.created)
        if apply_date not in apply_dates:
            apply_dates.append(apply_date)
        current_data = {
            'candidate': application.candidate.username,
            'apply_date': apply_date,
            'apply_time': datetime.datetime.time(application.created),
            'apply_year': apply_date.year,
            'apply_month': apply_date.strftime("%B"),
            'apply_day': apply_date.day,
        }
        candidates_per_apply_dates.append(current_data)
    return candidates_per_apply_dates, apply_dates


def applications_per_period(candidates_per_test, labels):
    applications = []
    for my_date in labels:
        cpt = 0
        for candidate in candidates_per_test:
            if candidate['apply_date'] == my_date:
                cpt += 1
        applications.append(cpt)
    return applications


class ParticipantForOffer(APIView):

    @check_offer_id
    def get(self, request, *args, **kwargs):
        if 'offer' in kwargs:
            offer = kwargs['offer']
            candidates = all_candidates_for_offer(offer)

            return Response(
                data={'candidates': candidates[0], 'length': candidates[1]},
                status=status.HTTP_200_OK
            )


class ParticipantForTest(APIView):

    @check_offer_id
    def get(self, request, *args, **kwargs):
        if 'offer' in kwargs:
            offer = kwargs['offer']
            tests = all_tests_for_offer(offer=offer)
            evaluations_for_offer = all_evaluations_for_offer(offer)
            data = get_data(tests, evaluations_for_offer)

            labels = data[1]
            chartData = data[2]
            chartLabel = "Nombre de questions repondues par test"

            data_set = {
                "labels": labels,
                "chartLabel": chartLabel,
                "chartData": chartData,
            }
            return Response(
                data=data_set,
                status=status.HTTP_200_OK
            )


def percentage_per_test(corrections_data):
    labels = []
    allChartData = []
    for item in corrections_data:
        test = Test.objects.get(id=item['test'])
        correction_per_candidate = item['correction_per_candidate']
        chartData = []
        for line in correction_per_candidate:
            candidate = Candidate.objects.get(id=line['candidate'])
            percentage = round(line['passed_percentage'], 2)
            if candidate.username not in labels:
                labels.append(candidate.username)
            chartData.append(percentage)
        data = {
            'chartData': chartData,
            'chartLabel': test.title
        }
        allChartData.append(data)
    return labels, allChartData


class ParticipantPercentagePerTest(APIView):
    @check_offer_id
    def get(self, request, *args, **kwargs):
        if 'offer' in kwargs:
            offer = kwargs['offer']
            evaluations_for_offer = all_evaluations_for_offer(offer)
            number_of_participants = candidates_from_evaluation(evaluations_for_offer)[0]
            evaluations_for_test = all_evaluations_for_test(offer)
            corrections_data = evaluation_correction(evaluations_for_test)
            data_set = percentage_per_test(corrections_data)

            labels = data_set[0]
            all_chart_data = data_set[1]

            data = {
                'labels': labels,
                'allChartData': all_chart_data
            }
            return Response(
                data=data,
                status=status.HTTP_200_OK
            )


class NumParticipantPerPeriod(APIView):
    @check_offer_id
    def get(self, request, *args, **kwargs):
        if 'offer' in kwargs:
            offer = kwargs['offer']
            appliances = Apply.objects.filter(offer=offer.id)
            apply_dates = get_applicants_per_period(appliances)[1]
            candidates_per_apply_dates = get_applicants_per_period(appliances)[0]
            labels = apply_dates
            chartLabel = "Applications Par Date"
            chartData = applications_per_period(candidates_per_apply_dates, apply_dates)
            data = {
                "labels": labels,
                "chartLabel": chartLabel,
                "chartData": chartData,
            }
            return Response(
                data=data,
                status=status.HTTP_200_OK
            )


class BestParticipantProfileForOffer(APIView):
    @check_offer_id
    def get(self, request, *args, **kwargs):
        if 'offer' in kwargs:
            offer = kwargs['offer']
            evaluations_for_offer = all_evaluations_for_offer(offer)
            number_of_participants = candidates_from_evaluation(evaluations_for_offer)[0]
            evaluations_for_test = all_evaluations_for_test(offer)
            corrections_data = evaluation_correction(evaluations_for_test)
            num_success_per_test = candidate_passed_test(corrections_data)[0]
            candidate_succeeded_all_test = candidate_passed_all_test(number_of_participants, num_success_per_test)
            return Response(
                data=candidate_succeeded_all_test,
                status=status.HTTP_200_OK
            )


class NumSuccessPerTestForOffer(APIView):
    @check_offer_id
    def get(self, request, *args, **kwargs):
        if 'offer' in kwargs:
            offer = kwargs['offer']
            evaluations_for_test = all_evaluations_for_test(offer)
            corrections_data = evaluation_correction(evaluations_for_test)
            num_success_per_test = candidate_passed_test(corrections_data)
            labels = num_success_per_test[1]
            chartLabel = "Nombre de passants par test"
            chartData = num_success_per_test[2]
            data = {
                "labels": labels,
                "chartLabel": chartLabel,
                "chartData": chartData,
            }
            return Response(
                data=data,
                status=status.HTTP_200_OK
            )


class NumFailurePerTestForOffer(APIView):
    @check_offer_id
    def get(self, request, *args, **kwargs):
        if 'offer' in kwargs:
            offer = kwargs['offer']
            evaluations_for_test = all_evaluations_for_test(offer)
            corrections_data = evaluation_correction(evaluations_for_test)
            num_failure_per_test = candidate_failed_test(corrections_data)

            labels = num_failure_per_test[1]
            chartLabel = "Nombre d'echoue par test"
            chartData = num_failure_per_test[2]
            data = {
                "labels": labels,
                "chartLabel": chartLabel,
                "chartData": chartData,
            }
            return Response(
                data=data,
                status=status.HTTP_200_OK
            )


class NumParticipantPerTest(APIView):

    @check_offer_id
    def get(self, request, *args, **kwargs):
        if 'offer' in kwargs:
            offer = kwargs['offer']
            candidates = candidate_participated_to_test(offer)
            candidates_per_test = candidates[0]

            labels = candidates[2]
            chartLabel = "Nombre de candidat par test"
            chartData = candidates[1]
            data = {
                "labels": labels,
                "chartLabel": chartLabel,
                "chartData": chartData,
            }
            return Response(
                data=data,
                status=status.HTTP_200_OK
            )


class OfferSuccessPercentage(APIView):
    pass
