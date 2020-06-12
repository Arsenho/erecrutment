from functools import wraps
from registration.models import Candidate, Employer
from rest_framework.response import Response
from rest_framework import status


def login_required_for_candidate(view_function):
    @wraps(view_function)
    def wrapped(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                candidate = Candidate.objects.get(id=request.user.id)
                kwargs['candidate'] = candidate
                return view_function(self, request, *args, **kwargs)
            except Candidate.DoesNotExist:
                return Response(
                    data={
                        'success': False,
                        'message': 'Please login as a candidate !'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            result = Response(
                data={
                    'success': False,
                    'message': 'Please login to continue'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
            return result

    return wrapped


def login_required_for_employer(view_function):
    @wraps(view_function)
    def wrapped(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                employer = Employer.objects.get(id=request.user.id)
                kwargs['employer'] = employer
                return view_function(self, request, *args, **kwargs)
            except Employer.DoesNotExist:
                if request.user.is_superuser:
                    return view_function(self, request, *args, **kwargs)
                else:
                    return Response(
                        data={
                            'success': False,
                            'message': 'Please login as the superuser or as an employer !'
                        },
                        status=status.HTTP_401_UNAUTHORIZED
                    )
        else:
            result = Response(
                data={
                    'success': False,
                    'message': 'Please login to continue'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
            return result

    return wrapped
