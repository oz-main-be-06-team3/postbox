from django.db import models

from constraints import Constraint
from users.models import Users


class Account(models.Model, Constraint):
    objects = None
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    account_num = models.CharField(max_length=20)  # 계좌번호
    # 은행 코드
    bank_code = models.IntegerField(default=Constraint.BANK_CODES)
    # 계좌 종류
    account_kind = models.CharField(max_length=20, choices=Constraint.ACCOUNT_TYPE)
    # 잔액
    balance = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        db_table = "account"
