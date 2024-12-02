from django.db import models

from constraints import Constraint
from PostBox.settings import base
from users.models import Users


class Account(models.Model, Constraint):
    objects = None
    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_num = models.CharField(max_length=20)  # 계좌번호
    # 은행 코드
    bank_code = models.CharField(max_length=5, choices=Constraint.BANK_CODES)
    # 계좌 종류
    account_kind = models.CharField(max_length=20, choices=Constraint.ACCOUNT_TYPE)
    # 잔액
    balance = models.IntegerField(null=False, blank=False, default=0)

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValueError("Accounts cannot be modified after creation.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.account_num

    class Meta:
        db_table = "account"
