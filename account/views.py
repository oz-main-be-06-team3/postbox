from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountSerializer


# 계좌 목록 조회 및 생성
class AccountListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        return render(request, "account_list_create.html", {"accounts": accounts})

    def post(self, request):
        data = {
            "account_num": request.POST.get("account_num"),
            "bank_code": request.POST.get("bank_code"),
            "account_kind": request.POST.get("account_kind"),
            "balance": 0,
        }
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return HttpResponseRedirect(reverse("account-list-create"))
        return render(request, "account_list_create.html", {"errors": serializer.errors})

    # 계좌 삭제


class AccountDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_id):
        account = get_object_or_404(Account, id=account_id, user=request.user)
        return render(request, "account_delete.html", {"account": account})

    def post(self, request, account_id):
        account = get_object_or_404(Account, id=account_id, user=request.user)
        account.delete()
        return HttpResponseRedirect(reverse("account-list-create"))
