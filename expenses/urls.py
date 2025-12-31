from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, SummaryView

router = DefaultRouter()
router.register(r"expenses", ExpenseViewSet, basename="expense")

urlpatterns = [
    path("", include(router.urls)),
    path("expenses/summary/weekly/", SummaryView.as_view(), {"period": "weekly"}, name="summary-weekly"),
    path("expenses/summary/monthly/", SummaryView.as_view(), {"period": "monthly"}, name="summary-monthly"),
]