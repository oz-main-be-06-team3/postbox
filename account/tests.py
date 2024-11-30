from django.contrib.auth import get_user_model
from django.test import TestCase

from constraints import Constraint

from .models import Account


class AccountModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass123", nickname="testuser", name="Test User"
        )

    def test_create_account(self):
        account = Account.objects.create(
            user=self.user,
            account_num="1234567890",
            bank_code=Constraint.BANK_CODES[0][0],
            account_kind=Constraint.ACCOUNT_TYPE[0][0],
            balance=1000,
        )
        self.assertIsInstance(account, Account)
        self.assertEqual(account.user, self.user)
        self.assertEqual(account.account_num, "1234567890")
        self.assertEqual(account.bank_code, Constraint.BANK_CODES[0][0])
        self.assertEqual(account.account_kind, Constraint.ACCOUNT_TYPE[0][0])
        self.assertEqual(account.balance, 1000)

    def test_account_str_method(self):
        account = Account.objects.create(
            user=self.user,
            account_num="1234567890",
            bank_code=Constraint.BANK_CODES[0][0],
            account_kind=Constraint.ACCOUNT_TYPE[0][0],
        )
        self.assertEqual(str(account), "1234567890")

    def test_account_default_balance(self):
        account = Account.objects.create(
            user=self.user,
            account_num="1234567890",
            bank_code=Constraint.BANK_CODES[0][0],
            account_kind=Constraint.ACCOUNT_TYPE[0][0],
        )
        self.assertEqual(account.balance, 0)

    def test_account_bank_code_choices(self):
        account = Account.objects.create(
            user=self.user,
            account_num="1234567890",
            bank_code=Constraint.BANK_CODES[0][0],
            account_kind=Constraint.ACCOUNT_TYPE[0][0],
        )
        self.assertIn(account.bank_code, dict(Constraint.BANK_CODES))

    def test_account_kind_choices(self):
        account = Account.objects.create(
            user=self.user,
            account_num="1234567890",
            bank_code=Constraint.BANK_CODES[0][0],
            account_kind=Constraint.ACCOUNT_TYPE[0][0],
        )
        self.assertIn(account.account_kind, dict(Constraint.ACCOUNT_TYPE))
