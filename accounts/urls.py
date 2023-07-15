from django.urls import path

from . import views
from . import signals

# urls here

urlpatterns = [
	path("register/", views.RegisterView.as_view(), name="register"),
	path("login/", views.LoginView.as_view(), name="login"),
]