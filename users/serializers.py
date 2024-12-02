import uuid

from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Users


class RegisterSerializer(serializers.ModelSerializer):
    email_verification_token = serializers.CharField(read_only=True)

    class Meta:
        model = Users
        fields = ["email", "nickname", "name", "password", "phone", "email_verification_token"]
        # extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value):
        # username 중복 확인
        if Users.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용 중인 사용자 이름입니다.")
        return value

    def create(self, validated_data):
        # email_verification_token은 생성자에 전달되지 않도록 제외
        validated_data["email_verification_token"] = uuid.uuid4().hex  # 고유 토큰 생성
        password = validated_data.pop("password")  # 비밀번호 처리
        user = Users(**validated_data)
        user.set_password(password)  # 비밀번호 암호화
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "email", "nickname", "name", "phone", "is_active", "staff", "admin"]
        read_only_fields = ["id", "is_active", "staff", "admin"]


# 회원정보 확인 및 수정/삭제
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["email", "nickname", "name", "phone"]


# user profile view
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message": "Deleted successfully"}, status=200)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # 사용자 상태 확인
        if not self.user.is_active:
            raise AuthenticationFailed("User account is disabled.", code="user_disabled")

        return data
