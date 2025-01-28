from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, WorkoutViewSet, SendLoginCodeView, VerifyLoginCodeView, CustomRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'workouts', WorkoutViewSet, basename='workout')
router.register(r'activities', ActivityViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
    path('refresh/', CustomRefreshView.as_view(), name='token_refresh'),
    path('send-login-code/', SendLoginCodeView.as_view(), name='send_login_code'),
    path('verify-login-code/', VerifyLoginCodeView.as_view(), name='verify_login_code'),
]