from django.urls import path

from . import views

urlpatterns = [
    path("portraits/", views.portraits, name="portraits"),
    path("add_commnet/", views.CommnetView.as_view(), name="post-commnet"),
    path("get_comments/<int:portrait_id_>", views.CommnetView.as_view(), name="post-commnet"),
]