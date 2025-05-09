from django.urls import path
from .views import TransactionView, BudgetView, CategoryChoicesView

urlpatterns = [
    path('transactions/', TransactionView.as_view(), name='transaction_list_create'),
    path('transactions/<int:transaction_id>/', TransactionView.as_view(), name='transaction_detail_update_delete'),
    path('budget/', BudgetView.as_view(), name='budget_list_create'),
    path('budget/<int:budget_id>/', BudgetView.as_view(), name='budget_detail_update_delete'),
    path('categories/', CategoryChoicesView.as_view(), name='category-choices'),
]
