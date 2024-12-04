from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import AccountDeleteView, AccountListCreateView

urlpatterns = [
    path('', AccountListCreateView.as_view(), name='account-list'),  # 계좌 목록 URL 정의
    path('delete/<int:account_id>/', AccountDeleteView.as_view(), name='account-delete'),
    path("jwt-test/", obtain_jwt_token),
]
