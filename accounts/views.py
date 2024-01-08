from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.exceptions import TokenError
import logging

logger = logging.getLogger(__name__)


from accounts.serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

User = get_user_model()




class UserViewset(GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    def get_serializer_class(self):
        if self.action == "create":
            return UserSerializer
        if self.action == "change_password":
            return UserChangePasswordSerializer
        if self.action == "forget_password":
            return ForgotPasswordSerializer
        return UserProfileSerializer

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        raise Http404

    def list(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)

    @action(detail=False, methods=["post"])
    def forget_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "An email is sent to your email address."})


logger = logging.getLogger(__name__)

class OTPVerification(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(email=email)
            if user.pin_code != otp:
                raise serializers.ValidationError("Invalid OTP.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")


        request.session['verified_user_email'] = email

        return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)


class ResetPassword(APIView):
    def post(self, request, format=None):
        email = request.session.get('verified_user_email')
        password = request.data.get('password')
        password1 = request.data.get('password1')

        if not email:
            return Response({"error": "Email not found in session."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(f"Changing password for user with email: {email}")

        if password == password1:
            user.set_password(password)
            user.save()
            return Response({"msg": "Password changed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
