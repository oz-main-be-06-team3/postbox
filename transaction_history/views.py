from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from account.models import Account

from .models import TransactionHistory
from .serializers import TransactionHistorySerializer


# 거래 목록 조회 및 생성
class TransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = TransactionHistory.objects.filter(account__user=request.user)
        return render(request, "transaction_list_create.html", {"transactions": transactions})

    def post(self, request):
        account_id = request.POST.get("account")
        account = get_object_or_404(Account, id=account_id, user=request.user)
        data = {
            "account": account.id,
            "transaction_type": request.POST.get("transaction_type"),
            "amount": request.POST.get("amount"),
        }
        serializer = TransactionHistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(reverse("transaction-list-create"))
        return render(request, "transaction_list_create.html", {"errors": serializer.errors})

    # 거래 상세 조회 및 수정


class TransactionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_id):
        transaction = get_object_or_404(TransactionHistory, id=transaction_id, account__user=request.user)
        return render(request, "transaction_detail.html", {"transaction": transaction})

    def post(self, request, transaction_id):
        transaction = get_object_or_404(TransactionHistory, id=transaction_id, account__user=request.user)
        data = {
            "transaction_type": request.POST.get("transaction_type", transaction.transaction_type),
            "amount": request.POST.get("amount", transaction.amount),
        }
        serializer = TransactionHistorySerializer(transaction, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(reverse("transaction-list-create"))
        return render(request, "transaction_detail.html", {"transaction": transaction, "errors": serializer.errors})

    # 거래 삭제


class TransactionDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_id):
        transaction = get_object_or_404(TransactionHistory, id=transaction_id, account__user=request.user)
        return render(request, "transaction_detail.html", {"transaction": transaction})

    def post(self, request, transaction_id):
        transaction = get_object_or_404(TransactionHistory, id=transaction_id, account__user=request.user)
        transaction.delete()
        return HttpResponseRedirect(reverse("transaction-list-create"))
