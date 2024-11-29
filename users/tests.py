from django.test import TestCase

from .models import Users

# Create your tests here.


class UsersTestCase(TestCase):

    def setUp(self):
        """Given: 각 테스트 전에 필요한 데이터 설정"""
        self.users_data = {
            "email": "test@example.com",
            "password": 1234,
            "nickname": "testuser",
            "name": "Test User",
            "phone": "1234567890",
            "last_login": "2024-11-29T10:50:00Z",
            "staff": "Manager",
            "admin": "SuperAdmin",
            "is_active": True,
        }

    def test_create_user(self):
        # When : 입력 받은 데이터를 바탕으로 유저 모델을 생성하면
        # user = Users.objects.create_user(**self.users_data)
        user = Users.objects.create_user(**self.users_data)
        # Then : 성공적으로 생성된 유저모델은 이메일, 닉네임, 비밀번호가 입력받은 데이터와 일치해야 한다.
        self.assertEqual(user.email, self.users_data["test@example.com"])
        self.assertEqual(user.nickname, self.users_data["testuser"])
        self.assertEqual(user.name, self.users_data["Test User"])
        self.assertEqual(user.phone, self.users_data["1234567890"])
        self.assertEqual(user.last_login, self.users_data["2024-11-29T10:50:00Z"])
        self.assertEqual(user.staff, self.users_data["Manager"])
        self.assertEqual(user.admin, self.users_data["SuperAdmin"])
        self.assertEqual(user.is_active, self.users_data["True"])
