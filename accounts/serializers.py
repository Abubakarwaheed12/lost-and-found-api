import string
import threading
from rest_framework import serializers
from rest_framework_simplejwt.tokens import SlidingToken
import random
from .emails import send_email
from accounts.models import User



class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True) 

    class Meta:
        model = User
        fields = ("email", "password", "confirm_password") 
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError("User with this email already exists.")
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("Password and Confirm Password do not match.")
        if len(attrs.get("password")) < 8:
            raise serializers.ValidationError("Password length should be at least 8 characters.")
        return super().validate(attrs)




 

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password', None)

        user = User.objects.create_user(**validated_data)

        subject = "Welcome to our Website!"
        text_content = "Welcome"
        recipient_list = [user.email]
        html_template = "email.html"
        context = {"name": user.email}

        thread = threading.Thread(target=send_email, args=(subject, text_content, recipient_list, html_template, context, True))
        thread.start()
        response = {
            "email": user.email,
            "token": SlidingToken.for_user(user),
            "message": "User Created Successfully"
        }
        return response

    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ("email", "password")



class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'profile_image')
    

class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField()
    password1 = serializers.CharField()

    class Meta:
        fields = ("old_password", "password", "password1")

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect")
        return old_password

    def validate(self, attrs):
        password = attrs.get("password")
        password1 = attrs.get("password1")
        if password != password1:
            raise serializers.ValidationError("Both Password Should be same.")
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['password'])
        user.save()
        return user



class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("email",)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is not exist in database.")
        return email
    
    def save(self, **validated_data):
        email = self.validated_data.get("email")
        user = User.objects.get(email=email)

        self.context['request'].session['reset_email'] = email

        # Generate a random 4-digit PIN code
        pin_code = ''.join(random.choices(string.digits, k=4))
        user.pin_code = pin_code
        user.save()

        subject = "Reset Password"
        text_content = "Hi"
        recipient_list = [email,]
        html_template = "reset_password.html"
        context = {"name": user.email, "pin_code": pin_code}
        thread = threading.Thread(target=send_email, args=(subject, text_content, recipient_list, html_template, context, True))
        thread.start()
        return user


    

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password1 = serializers.CharField()
    otp = serializers.CharField()  

    class Meta:
        fields = ("password", "password1", "otp")

    def validate(self, attrs):
        password = attrs.get("password")
        password1 = attrs.get("password1")
        otp = attrs.get("otp")

        if password != password1:
            raise serializers.ValidationError("Both Passwords Should be the same.")

        user = self.context.get("user")  
        if not user or user.pin_code != otp:
            raise serializers.ValidationError("Invalid OTP.")

        return attrs

    def save(self, **kwargs):
        user = self.context.get("user")
        user.set_password(self.validated_data['password'])
        user.save()
        return user

