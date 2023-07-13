from django.urls import path, include

urlpatterns = [
    path("portrait/", include("portrait.urls")),
    path("accounts/", include("accounts.urls")),
]