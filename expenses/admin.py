from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "amount", "date", "created_at")
    list_filter = ("category", "date")
    search_fields = ("user__username", "description")
    ordering = ("-date", "-created_at")
