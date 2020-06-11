from django.shortcuts import render
from rest_framework import generics


# Create your views here.

class CompanyView(generics.ListCreateAPIView):
    """
    This view allow et get and post request.
    It gives the possibility to get all companies and also to create a new company
    """
