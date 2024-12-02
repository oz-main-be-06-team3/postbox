from rest_framework import serializers

from transaction_history.models import TransactionHistory


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = "__all__"
        read_only_fields = ("id",)
