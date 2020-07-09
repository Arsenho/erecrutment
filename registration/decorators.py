from functools import wraps

from rest_framework.response import Response
from rest_framework import status

from registration.serializers import UserMiniSerializer


def already_logged_in(view_method):
    @wraps(view_method)
    def _wrapped(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_method(self, request, *args, **kwargs)
        else:
            user = UserMiniSerializer(request.user).data
            return Response(
                data={
                    'logged': True,
                    'user': user,
                    'message': 'utilisateur deja authentifie'
                },
                status=status.HTTP_302_FOUND
            )
    return _wrapped
