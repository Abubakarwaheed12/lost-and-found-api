from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import re
from django.core.exceptions import ValidationError


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    forget_password_token= models.CharField(max_length=255,  null=True , blank=True)
    
    email_token = models.CharField(max_length=200, null=True, blank=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
    
    
   
    
