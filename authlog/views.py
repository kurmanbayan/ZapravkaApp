from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.core import serializers

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid data'})
    token, created = Token.objects.get_or_create(user=user)
    user_info = {
        "username": user.username,
        "email": user.email,
        "pk": user.pk
    }
    return Response({'code': 0, 'token': token.key, 'user': user_info})

@api_view(['POST'])
def register(request): 
    userName = request.data.get('username', None)
    userPass = request.data.get('password', None)
    userMail = request.data.get('email', None)

    isEmailExists = not User.objects.all().filter(email=userMail)
    isUsernameExists = not User.objects.all().filter(username=userName)
    
    if not isEmailExists:
        return Response({"code": 1, "message": "The email address you have entered is already registered"})
    elif not isUsernameExists:
        return Response({"code": 1, "message": "The username you have entered is already registered"})

    user = User.objects.create(username=userName, email=userMail)
    user.set_password(userPass)
    user.save()
    return Response({"code": 0, "message": "User successfully created"})