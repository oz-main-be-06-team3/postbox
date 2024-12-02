from django.urls import path

from .views import (
    TransactionDeleteView,
    TransactionDetailView,
    TransactionListCreateView,
)

urlpatterns = [
    path("", TransactionListCreateView.as_view(), name="transaction-list-create"),
    path("<int:transaction_id>/", TransactionDetailView.as_view(), name="transaction-detail"),
    path("<int:transaction_id>/delete/", TransactionDeleteView.as_view(), name="transaction-delete"),
]
