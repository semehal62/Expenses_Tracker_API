from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Optional root welcome view
def home(request):
    return JsonResponse({"message": "Welcome to Expenses Tracker API"})

urlpatterns = [
    path("", home),  # <-- root URL
    path("admin/", admin.site.urls),

    # API schema & docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),

    # Accounts and Expenses APIs
    path("api/accounts/", include("accounts.urls")),  # register/login/logout + ban
    path("api/expenses/", include("expenses.urls")),  # expenses CRUD + filters + summaries
]
