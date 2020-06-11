from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import mixins
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class CompanyList(generics.ListCreateAPIView):
    """
    This view allow et get and post request.
    It gives the possibility to get all companies and also to create a new company
    """

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
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
        else:
            return Response(
                data={'message': 'please login as employer'},
                status=status.HTTP_401_UNAUTHORIZED
            )
