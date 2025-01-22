from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Activity, Workout
from .serializers import ActivitySerializer, WorkoutSerializer
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)


class SendLoginCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user, created = User.objects.get_or_create(email=email, defaults={'username': email})
        code = random.randint(100000, 999999)
        user.profile.login_code = code
        user.profile.save()
        
        return Response({'message': 'Login code sent', 'code': code}, status=status.HTTP_200_OK)
    
class VerifyLoginCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            user = User.objects.get(email=email)
            if user.profile.login_code == code:
                user.profile.login_code = ''
                user.profile.save()
                login(request, user)
                refresh = RefreshToken.for_user(user)
                response = Response({
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    secure=True,
                    path='refresh/',
                    samesite='Strict'
                )
                return response
            return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class CustomRefreshView(TokenRefreshView):
    def get(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({'error':'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data={'refresh':refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        return Response(serializer.validated_data, status=status.HTTP_200_OK)