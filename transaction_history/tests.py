from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.utils import timezone

from account.models import Account
from constraints import Constraint

from .models import TransactionHistory


class TransactionHistoryTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="test@example.com", nickname="testuser", name="Test User", password="testpassword"
        )
        self.account = Account.objects.create(user=self.user)

    def test_create_transaction_history(self):
        transaction = TransactionHistory.objects.create(
            account=self.account,
            amount=1000,
            after_amount=5000,
            account_title="Test Account",
            dw_type=Constraint.TRANSACTION_TYPE[0][0],
            amount_type=Constraint.TRANSACTION_METHOD[0][0],
        )
        self.assertIsNotNone(transaction.id)
        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.amount, 1000)
        self.assertEqual(transaction.after_amount, 5000)
        self.assertEqual(transaction.account_title, "Test Account")
        self.assertEqual(transaction.dw_type, Constraint.TRANSACTION_TYPE[0][0])
        self.assertEqual(transaction.amount_type, Constraint.TRANSACTION_METHOD[0][0])
        self.assertIsNotNone(transaction.transaction_at)

    def test_transaction_history_str_method(self):
        transaction = TransactionHistory.objects.create(
            account=self.account,
            amount=1000,
            after_amount=5000,
            account_title="Test Account",
            dw_type=Constraint.TRANSACTION_TYPE[0][0],
            amount_type=Constraint.TRANSACTION_METHOD[0][0],
        )
        expected_str = f"{transaction.account_title} - {transaction.amount}"
        self.assertEqual(str(transaction), expected_str)

    def test_transaction_history_constraints(self):
        transaction = TransactionHistory.objects.create(
            account=self.account,
            amount=1000,
            after_amount=5000,
            account_title="Test Account",
            dw_type=Constraint.TRANSACTION_TYPE[0][0],
            amount_type=Constraint.TRANSACTION_METHOD[0][0],
        )
        self.assertIn(transaction.dw_type, dict(Constraint.TRANSACTION_TYPE))
        self.assertIn(transaction.amount_type, dict(Constraint.TRANSACTION_METHOD))

    def test_transaction_history_auto_now_add(self):
        before = timezone.now()
        transaction = TransactionHistory.objects.create(
            account=self.account,
            amount=1000,
            after_amount=5000,
            account_title="Test Account",
            dw_type=Constraint.TRANSACTION_TYPE[0][0],
            amount_type=Constraint.TRANSACTION_METHOD[0][0],
        )
        after = timezone.now()
        self.assertTrue(before <= transaction.transaction_at <= after)
