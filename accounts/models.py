from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from uuid import uuid4
from django.contrib.auth import password_validation

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if username is None:
            raise ValueError('Username is required.')
        if email is None:
            raise ValueError('Email is required.')
        
        if password:
            try:
                password_validation.validate_password(password)

            except Exception as e:
                raise ValueError(e)
        email = self.normalize_email(email)
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

        
    

    def create_superuser(self, username, email, password=None, **extra_fields):
        if password is None:
            raise ValueError('Password is required.')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)




class UserModel(AbstractBaseUser):
    userID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','password']

    def __str__(self):
        return self.username
    

class ForgotPasswordMapping(models.Model):
    userID = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)