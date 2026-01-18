from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, SummaryView

router = DefaultRouter()
router.register(r"", ExpenseViewSet, basename="expense")

urlpatterns = [
    path("", include(router.urls)),
    path("summary/weekly/", SummaryView.as_view(), {"period": "weekly"}, name="summary-weekly"),
    path("summary/monthly/", SummaryView.as_view(), {"period": "monthly"}, name="summary-monthly"),
]
