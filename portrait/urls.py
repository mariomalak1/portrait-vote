from django.urls import path

from . import views

urlpatterns = [
    path("portraits/", views.Portratis.as_view(), name="portraits"),
    path("comments/", views.CommnetView.as_view(), name="post-commnet"),
    path("portrait_detail/", views.PortraitDetails.as_view(), name="portrait-detail"),
    path("vote_portrait/", views.VoteView.as_view(), name="vote-portrait"),
]