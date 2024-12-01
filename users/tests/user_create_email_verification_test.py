from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserModelTests(APITestCase):
    def test_user_creation(self):
        """
        사용자 생성 테스트
        """
        user = User.objects.create_user(
            email="testuser@example.com", nickname="testuser", name="Test User", password="testpassword123"
        )
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("testpassword123"))

    def test_email_verification_token(self):
        """
        이메일 인증 토큰 생성 테스트
        """
        user = User.objects.create_user(
            email="verifyuser@example.com", nickname="verifyuser", name="Verify User", password="verify123"
        )
        self.assertIsNotNone(user.email_verification_token)
        self.assertFalse(user.is_active)


class RegistrationTests(APITestCase):
    def test_user_registration(self):
        """
        회원가입 API 테스트
        """
        data = {
            "email": "newuser@example.com",
            "nickname": "newuser",
            "name": "New User",
            "password": "securepassword123",
        }
        response = self.client.post("/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email_verification_token", response.data)

    def test_invalid_registration(self):
        """
        잘못된 회원가입 요청 테스트
        """
        data = {"email": "", "nickname": "newuser", "name": "New User", "password": "securepassword123"}  # 이메일 없음
        response = self.client.post("/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="loginuser@example.com", nickname="loginuser", name="Login User", password="testpassword123"
        )

    def test_jwt_login(self):
        """
        JWT 로그인 API 테스트
        """
        data = {"email": "loginuser@example.com", "password": "testpassword123"}
        response = self.client.post("/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_login(self):
        """
        잘못된 로그인 요청 테스트
        """
        data = {"email": "loginuser@example.com", "password": "wrongpassword"}
        response = self.client.post("/login/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


from rest_framework_simplejwt.tokens import RefreshToken


class LogoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="logoutuser@example.com", nickname="logoutuser", name="Logout User", password="testpassword123"
        )
        self.client.login(email="logoutuser@example.com", password="testpassword123")
        refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(refresh)

    def test_jwt_logout(self):
        """
        JWT 로그아웃 API 테스트
        """
        data = {"refresh": self.refresh_token}
        response = self.client.post("/logout/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logout successful")

    def test_invalid_logout(self):
        """
        잘못된 로그아웃 요청 테스트
        """
        data = {"refresh": "invalidtoken"}
        response = self.client.post("/logout/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
