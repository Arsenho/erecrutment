from rest_framework import status
from rest_framework.response import Response

from registration.models import Candidate


class LoginRequiredForCandidate(object):
    """Verify if the current user is authenticate and is a candidate"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or \
                (not isinstance(request.user, Candidate)):
            result = Response(
                data={
                    'success': False,
                    'message': 'credentials non authorized ! Login as a candidate'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().dispatch(request, *args, **kwargs)