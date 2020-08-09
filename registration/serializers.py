from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib.auth.models import Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        user.save()
        return user


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'


class EmployerMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = [
            'id',
            'email',
            'username',
            'last_name',
            'first_name',
            'gender',
            'phone_number',
            'groups',
            'is_active',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'read_only': True},
            'is_active': {'read_only': True},
        }

    def create(self, validated_data):
        employer = Employer(
            email=validated_data['email'],
            username=validated_data['username'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name'],
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number'],
            password=make_password(validated_data['password'])
        )
        employer.save()
        return employer


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class CandidateMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            'id',
            'email',
            'username',
            'last_name',
            'first_name',
            'gender',
            'phone_number',
            'groups',
            'is_active',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'read_only': True},
            'is_active': {'read_only': True},
        }

    def create(self, validated_data):
        candidate = Candidate(
            email=validated_data['email'],
            username=validated_data['username'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name'],
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number'],
            password=make_password(validated_data['password'])
        )
        candidate.save()
        return candidate


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'username': {'read_only': True},
            'password': {'read_only': True},
        }
