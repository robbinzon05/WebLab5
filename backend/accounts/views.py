# accounts/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from django.contrib.auth.models import User

# backend/accounts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    avatar_id = request.data.get('avatar_id')

    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.set_password(password)
    if avatar_id:
        user.last_name = avatar_id  # Сохраняем avatar_id в last_name

    user.save()
    return Response({'detail': 'Профиль успешно обновлен.'})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Добавляем данные о пользователе
        data['user'] = UserSerializer(self.user).data

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer