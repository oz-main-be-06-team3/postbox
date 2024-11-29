from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from transaction_history.models import TransactionHistory


class TransactionHistoryTest(TestCase):
    def setUp(self):
        # 테스트용 사용자 생성
        self.user = User.objects.create(
            email="test@example.com", password="testpass123", nickname="테스트", name="김테스트", phone="0101234567"
        )

        # 테스트용 계좌 생성
        self.account = Account.objects.create(
            user=self.user, account_num="1234567890", bank_code=1, account_kind="SAVINGS", balance=10000
        )

    def test_create_transaction(self):
        # 거래 내역 생성 테스트
        transaction = TransactionHistory.objects.create(
            account=self.account,
            amount=5000,
            after_amount=15000,
            account_title="테스트 거래",
            dw_type="DEPOSIT",
            amount_type="CASH",
        )

        self.assertEqual(transaction.amount, 5000)
        self.assertEqual(transaction.after_amount, 15000)
        self.assertEqual(transaction.account_title, "테스트 거래")
        self.assertEqual(transaction.dw_type, "DEPOSIT")
        self.assertEqual(transaction.amount_type, "CASH")
        self.assertTrue(isinstance(transaction.transaction_at, timezone.datetime))

    def test_transaction_types(self):
        # 거래 유형 검증
        transaction = TransactionHistory.objects.create(
            account=self.account,
            amount=1000,
            after_amount=11000,
            account_title="거래 유형 테스트",
            dw_type="WITHDRAWAL",
            amount_type="CARD",
        )

        self.assertIn(transaction.dw_type, dict(TransactionHistory.TRANSACTION_TYPES))
        self.assertIn(transaction.amount_type, dict(TransactionHistory.AMOUNT_TYPES))

    def test_invalid_transaction_type(self):
        # 잘못된 거래 유형 테스트
        with self.assertRaises(Exception):
            TransactionHistory.objects.create(
                account=self.account,
                amount=1000,
                after_amount=11000,
                account_title="잘못된 거래 유형",
                dw_type="INVALID",
                amount_type="CASH",
            )

    def test_account_relationship(self):
        # 계좌와의 관계 테스트
        transaction = TransactionHistory.objects.create(
            account=self.account,
            amount=2000,
            after_amount=12000,
            account_title="계좌 관계 테스트",
            dw_type="DEPOSIT",
            amount_type="TRANSFER",
        )

        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.account.user, self.user)
