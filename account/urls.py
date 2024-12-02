from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import AccountDeleteView, AccountListCreateView

urlpatterns = [
    path("", AccountListCreateView.as_view(), name="account-list-create"),
    path("<int:account_id>/delete/", AccountDeleteView.as_view(), name="account-delete"),
    path("jwt-test/", obtain_jwt_token),
]
