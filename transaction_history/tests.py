from django.test import TestCase
from django.utils import timezone

from account.models import Account
from constraints import Constraint
from users.models import Users

from .models import TransactionHistory


class TransactionHistoryTest(TestCase):
    def setUp(self):
        # 테스트용 사용자 생성
        self.user = Users.objects.create(
            email="test@example.com", password="testpass123", nickname="테스트", name="김테스트", phone="0101234567"
        )

        # 테스트용 계좌 생성
        self.account = Account.objects.create(
            user=self.user, account_num=1234567890, bank_code=1, account_kind="CHECKING", balance=10000
        )

        # 테스트용 거래내역 데이터
        self.transaction_data = {
            "account": self.account,
            "amount": 5000,
            "after_amount": 15000,
            "account_title": "테스트 거래",
            "dw_type": "DEPOSIT",
            "amount_type": "TRANSFER",
            "transaction_at": timezone.now(),
        }

    def test_create_transaction(self):
        # 거래내역 생성 테스트
        transaction = TransactionHistory.objects.create(**self.transaction_data)

        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.amount, self.transaction_data["amount"])
        self.assertEqual(transaction.after_amount, self.transaction_data["after_amount"])
        self.assertEqual(transaction.account_title, self.transaction_data["account_title"])
        self.assertEqual(transaction.dw_type, self.transaction_data["dw_type"])
        self.assertEqual(transaction.amount_type, self.transaction_data["amount_type"])
        self.assertTrue(isinstance(transaction.transaction_at, timezone.datetime))

    def test_transaction_types(self):
        # 거래 유형 검증
        transaction = TransactionHistory.objects.create(**self.transaction_data)
        self.assertIn(transaction.dw_type, dict(Constraint.TRANSACTION_TYPE))
        self.assertIn(transaction.amount_type, dict(Constraint.TRANSACTION_METHOD))

    def test_invalid_transaction_type(self):
        # 잘못된 거래 유형 테스트
        invalid_data = self.transaction_data.copy()
        invalid_data["dw_type"] = "INVALID"

        with self.assertRaises(Exception):
            TransactionHistory.objects.create(**invalid_data)

    def test_account_relationship(self):
        # 계좌와의 관계 테스트
        transaction = TransactionHistory.objects.create(**self.transaction_data)

        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.account.user, self.user)

    def test_cascade_deletion(self):
        # 계좌 삭제 시 연관된 거래내역도 삭제되는지 테스트
        transaction = TransactionHistory.objects.create(**self.transaction_data)
        transaction_id = transaction.id

        self.account.delete()

        with self.assertRaises(TransactionHistory.DoesNotExist):
            TransactionHistory.objects.get(id=transaction_id)
