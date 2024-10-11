from django.urls import path
from . import views
from django.http import Http404
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "user/<int:user_id>/", views.user_detail, name="user_detail"
    ),  # Dynamic user page
    path("user/", views.page_not_found),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("search/", views.search_user, name="search_user"),
    path("profile/<str:username>/", views.profile_page, name="profile"),
    path("upload/", views.upload, name="upload"),
    path("sample/<int:sample_id>/", views.sample_player, name="sample_player"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
