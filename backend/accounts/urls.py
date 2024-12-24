# backend/accounts/urls.py

from django.urls import path
from .views import RegisterView, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

# backend/accounts/urls.py
from django.urls import path
from .views import RegisterView, MyTokenObtainPairView, update_profile

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('update/', update_profile, name='update_profile'),  # Добавьте этот маршрут
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
