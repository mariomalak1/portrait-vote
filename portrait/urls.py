from django.urls import path

from . import views

urlpatterns = [
    path("portraits/", views.portraits, name="portraits")
]