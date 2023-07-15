from django.urls import path

from . import views

urlpatterns = [
    path("portraits/", views.Portratis.as_view(), name="portraits"),
    path("comments/", views.CommnetView.as_view(), name="post-commnet"),
]