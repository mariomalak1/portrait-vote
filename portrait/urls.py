from django.urls import path

from .views import rr

urlpatterns = [
    path("ks/", rr)
]