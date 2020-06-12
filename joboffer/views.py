from django.contrib.auth.models import Group
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .decorators import login_required_for_candidate, login_required_for_employer

# Create your views here.
from joboffer.models import Company, Offer, Apply
from joboffer.serializers import CompanySerializer, OfferSerializer, ApplySerializer
from registration.models import User
from registration.serializers import UserSerializer


class CompanyList(generics.ListCreateAPIView):
    """
    This view allow et get and post request.
    It gives the possibility to get all companies and also to create a new company
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    # the user must be logged either as an employer or as a superuser
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


def createAttachments(request):
    if 'files' in request.data:
        pass


class OfferList(generics.ListCreateAPIView):
    """
    this view allows the creation of a new instance of Offer and
    also allows to get all Offer
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    @login_required_for_employer
    def post(self, request, *args, **kwargs):
        group_admin = Group.objects.get(name='admin')
        group_employer = Group.objects.get(name='employer')
        user = UserSerializer(request.user)
        print(user.data)
        if (group_admin.id in user.data['groups']) or \
                (group_employer.id in user.data['groups']):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['published_by'] = request.user
            print(serializer.validated_data)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        else:
            return Response(
                data={'message': 'please login as employer or superuser'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class ApplyList(generics.ListCreateAPIView):
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer

    # redefine the post method to managing the cv file
    # only a candidate can apply for a job offer
    @login_required_for_candidate
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # the authenticated user must be a candidate
        serializer.validated_data['candidate'] = kwargs['candidate']
        self.perform_create(serializer)

        # get serializer success headers
        headers = self.get_success_headers(serializer.data)

        # return newly created apllication
        return Response(
            data={'success': True, 'message': 'vous avez postule avec succes'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

