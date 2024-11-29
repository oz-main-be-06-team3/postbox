from django.db import models

from account.models import Account
from constraints import Constraint


class TransactionHistory(models.Model, Constraint):
    objects = None
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.IntegerField()
    after_amount = models.IntegerField()
    account_title = models.CharField(max_length=255)
    dw_type = models.CharField(max_length=10, choices=Constraint.TRANSACTION_TYPE)
    amount_type = models.CharField(max_length=20, choices=Constraint.TRANSACTION_METHOD)
    transaction_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_title} - {self.amount}"

    class Meta:
        db_table = "transaction_history"
