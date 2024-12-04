from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from .models import Account
from .serializers import AccountSerializer
from django.contrib import messages


# 계좌 목록 조회 및 생성
class AccountListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 현재 사용자 계좌 조회
        accounts = Account.objects.filter(user=request.user)
        serializer = AccountSerializer(accounts, many=True)
        return render(request, 'account_list.html', {'accounts': serializer.data})

    def post(self, request):
        # POST 데이터 가져오기
        data = {
            "account_num": request.data.get("account_num"),
            "bank_code": request.data.get("bank_code"),
            "account_kind": request.data.get("account_kind"),
            "balance": 0,  # 기본값 설정
        }

        # Serializer로 데이터 검증 및 저장
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            # 성공 시 리스트 페이지로 리다이렉트
            return HttpResponseRedirect(reverse("account-list-create"))

        # 실패 시 오류와 함께 다시 렌더링
        accounts = Account.objects.filter(user=request.user)
        return render(request, "account_create.html", {"accounts": accounts, "errors": serializer.errors}
                      )
    # 계좌 삭제


class AccountDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_id):
        # 계좌 조회 및 삭제 확인 페이지 렌더링
        account = get_object_or_404(Account, id=account_id, user=request.user)
        return render(request, "account_confirm_delete.html", {"account": account})

    def post(self, request, account_id):
        # 계좌 삭제
        account = get_object_or_404(Account, id=account_id, user=request.user)
        account.delete()
        # 성공 메시지 추가
        messages.success(request, "Account has been successfully deleted.")
        return HttpResponseRedirect(reverse("account-list"))
