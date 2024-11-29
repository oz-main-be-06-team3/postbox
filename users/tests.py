from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", nickname="normal", name="Normal User", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertEqual(user.nickname, "normal")
        self.assertEqual(user.name, "Normal User")
        self.assertTrue(user.is_active)
        self.assertFalse(user.staff)
        self.assertFalse(user.admin)
        self.assertTrue(user.check_password("foo"))

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", nickname="super", name="Super User", password="foo"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertEqual(admin_user.nickname, "super")
        self.assertEqual(admin_user.name, "Super User")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.staff)
        self.assertTrue(admin_user.admin)
        self.assertTrue(admin_user.check_password("foo"))

    def test_create_user_without_email(self):
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", nickname="test", name="Test User", password="foo")

    def test_create_user_with_invalid_email(self):
        User = get_user_model()
        with self.assertRaises(ValidationError):
            user = User.objects.create_user(email="invalid", nickname="test", name="Test User", password="foo")
            user.full_clean()

    def test_email_normalized(self):
        User = get_user_model()
        email = "test@EXAMPLE.COM"
        user = User.objects.create_user(email=email, nickname="test", name="Test User", password="foo")
        self.assertEqual(user.email, email.lower())

    def test_user_string_representation(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@example.com", nickname="test", name="Test User", password="foo")
        self.assertEqual(str(user), "test@example.com")

    def test_user_fields(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="test@example.com", nickname="test", name="Test User", password="foo", phone="1234567890"
        )
        self.assertEqual(user.phone, "1234567890")
        self.assertIsNone(user.last_login)

    def test_username_field_not_used(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@example.com", nickname="test", name="Test User", password="foo")
