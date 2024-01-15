
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ResetPassword, UserViewset, OTPVerification, UserProfileUpdateView
from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView

app_name = "accounts"

router = DefaultRouter()
router.register('user', UserViewset, basename='signup')


urlpatterns = [
    path("login/", TokenObtainSlidingView.as_view(), name="login"),
    path("profile/update/", UserProfileUpdateView.as_view(), name='user-profile-update'),
    path("refresh/", TokenRefreshSlidingView.as_view(), name="refresh"),
    path("reset/", ResetPassword.as_view(), name="reset"),
    path("verify/", OTPVerification.as_view(), name="verify"),

] + router.urls

