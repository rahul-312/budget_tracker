from django.urls import path
from .views import TransactionView, BudgetView, CategoryChoicesView, BudgetSummaryView,SpendingByCategoryView, TotalExpensesOverTimeAPIView

urlpatterns = [
    path('transactions/', TransactionView.as_view(), name='transaction_list_create'),
    path('transactions/<int:transaction_id>/', TransactionView.as_view(), name='transaction_detail_update_delete'),
    path('budget/', BudgetView.as_view(), name='budget_list_create'),
    path('budget/<int:budget_id>/', BudgetView.as_view(), name='budget_detail_update_delete'),
    path('categories/', CategoryChoicesView.as_view(), name='category-choices'),
    path('budget-summary/', BudgetSummaryView.as_view(), name='budget_summary'),
    path('spending-by-category/', SpendingByCategoryView.as_view(), name='spending-by-category'),
    path('total-expenses-over-time/', TotalExpensesOverTimeAPIView.as_view(), name='total-expenses-over-time'),
]
