from django.contrib.auth.models import Group
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .decorators import login_required_for_candidate, \
    login_required_for_employer

# Create your views here.
from joboffer.models import Company, Offer, Apply, TestForOffer
from joboffer.serializers import CompanySerializer, OfferSerializer, ApplySerializer, TestForOfferSerializer
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
        print(request.data)
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


class OfferDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

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


class TestForOfferList(generics.ListCreateAPIView):
    queryset = TestForOffer.objects.all()
    serializer_class = TestForOfferSerializer


class TestForOfferDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestForOffer.objects.all()
    serializer_class = TestForOfferSerializer


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


class OfferCategoryList(APIView):
    serializer_class = OfferSerializer

    def get(self, request, *args, **kwargs):
        categories = Offer.CATEGORY_TYPE
        offer_categories = []
        for item in categories:
            if item[0] != 'aucune':
                offer_categories.append(item[1])
        return Response(
            data=offer_categories,
            status=status.HTTP_200_OK
        )
