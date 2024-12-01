from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer

from .models import Users
from .serializers import RegisterSerializer, UserProfileSerializer, UserSerializer


def home(request):
    return HttpResponse("<h1>Welcome to the Home Page</h1>")


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class RegisterView(APIView):
    def get(self, request):
        # GET 요청 시 HTML 템플릿 렌더링
        return render(request, "register.html")

    def post(self, request):
        # POST 요청 처리
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공"}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def get(self, request):
        # GET 요청 시 HTML 템플릿 렌더링
        print("Rendering login.html")
        return render(request, "login.html")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            # Access 및 Refresh 토큰을 쿠키에 저장
            response.set_cookie(
                key="access_token",
                value=data["access"],
                httponly=True,
                secure=True,  # HTTPS만 허용 (개발 시 False로 설정 가능)
                samesite="Lax",  # SameSite 속성
            )
            response.set_cookie(
                key="refresh_token",
                value=data["refresh"],
                httponly=True,
                secure=True,
                samesite="Lax",
            )
            # 본문에서 토큰을 제거 (옵션)
            del response.data["access"]
            del response.data["refresh"]
        return response


class TokenRefreshView(TokenRefreshView):
    pass


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # GET 요청 시 HTML 템플릿 렌더링
        return render(request, "logout.html")

    def post(self, request):
        # Refresh Token 가져오기
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=400)
        try:
            # Refresh Token 블랙리스트에 추가
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # GET 요청 시 HTML 템플릿 렌더링
        return render(request, "profile.html", {"user": request.user})

    def post(self, request):
        # 프로필 수정
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "프로필 수정 완료"}, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        # 계정 삭제
        request.user.delete()
        return Response({"message": "Deleted successfully"}, status=200)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer