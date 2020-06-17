from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from registration.models import User, Candidate, Employer
from registration.serializers import UserSerializer, UserMiniSerializer, CandidateSerializer, CandidateMiniSerializer, \
    EmployerSerializer, EmployerMiniSerializer
from rest_framework.decorators import api_view


class UserList(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserMiniList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserMiniSerializer


class CandidateList(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateMiniList(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateMiniSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get the candidate instance
        candidate = serializer.save()
        group = Group.objects.get(name='candidate')

        # set the candidate's groups
        candidate.groups.set([group.id])

        # save candidate with groups instance
        candidate.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class EmployerList(generics.ListCreateAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer


class EmployerMiniList(generics.ListCreateAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerMiniSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get the employer instance
        employer = serializer.save()
        group = Group.objects.get(name='employer')

        # set the employer's groups
        employer.groups.set([group.id])
        employer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class Login(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = UserMiniSerializer(request.user)
            return Response(
                data=user.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={'error': 'Veuillez vous connecter svp !'},
                status=status.HTTP_200_OK
            )

    def post(self, request, *args, **kwargs):
        username, password = '', ''
        print(request.data)
        if 'username' in request.data and 'password' in request.data:
            username = request.data['username']
            password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(
                data=UserSerializer(user).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={'error': 'Username ou Mot de passe incorrect !'},
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['GET'])
def logout_view(request):
    if request.user.is_authenticated:
        user = request.user
        logout(request)
        return Response(data=UserSerializer(user).data)
    else:
        return Response(data={'authenticated': False})
