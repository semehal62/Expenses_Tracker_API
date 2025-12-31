from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import Expense
from .serializers import ExpenseSerializer
from .permissions import NotBanned

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, NotBanned]

    def get_queryset(self):
        user = self.request.user
        queryset = Expense.objects.all() if getattr(user, "is_admin", False) else Expense.objects.filter(user=user)

        category = self.request.query_params.get("category")
        date_str = self.request.query_params.get("date")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if category:
            queryset = queryset.filter(category=category)
        if date_str:
            queryset = queryset.filter(date=date_str)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.user and not getattr(self.request.user, "is_admin", False):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only modify your own expenses.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.user and not getattr(request.user, "is_admin", False):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own expenses.")
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="category/(?P<category>[^/]+)")
    def by_category(self, request, category=None):
        qs = self.get_queryset().filter(category=category)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="date/(?P<date>\\d{4}-\\d{2}-\\d{2})")
    def by_date(self, request, date=None):
        qs = self.get_queryset().filter(date=date)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class SummaryView(APIView):
    permission_classes = [IsAuthenticated, NotBanned]

    def get(self, request, period: str):
        user = request.user
        qs = Expense.objects.all() if getattr(user, "is_admin", False) else Expense.objects.filter(user=user)

        if period not in ("weekly", "monthly"):
            return Response({"detail": "period must be 'weekly' or 'monthly'"}, status=status.HTTP_400_BAD_REQUEST)

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        if start_date and end_date:
            qs = qs.filter(date__range=[start_date, end_date])

        totals = qs.values("category").annotate(total=Sum("amount")).order_by("category")
        return Response({"period": period, "totals": list(totals)})