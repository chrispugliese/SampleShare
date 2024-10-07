from django.urls import path
from . import views
from django.http import Http404

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "user/<int:user_id>/", views.user_detail, name="user_detail"
    ),  # Dynamic user page
    path("user/", views.page_not_found),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("sample/<int:sample_id>/", views.sample_player, name="sample_player"),
]

