from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, name, password=None, **extra_fields):
        extra_fields.setdefault("staff", True)
        extra_fields.setdefault("admin", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, nickname, name, password, **extra_fields)


class Users(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    email_verification_token = models.CharField(max_length=32, blank=True, null=True)  # 이메일 인증 토큰 필드
    password = models.CharField(max_length=128, null=False)
    nickname = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=20, null=False)
    last_login = models.DateTimeField(null=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
