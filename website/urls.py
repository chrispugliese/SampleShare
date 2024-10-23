from .views import CreatePostView, send_friend_request, accept_friend_request, decline_friend_request, remove_friend, private_chat_redirect
from django.urls import path
from . import views
from django.http import Http404
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path("", views.home, name="home"),
	path("login/", views.login_user, name="login"),
	path("logout/", views.logout_user, name="logout"),
	path("register/", views.register_user, name="register"),
	path("search/", views.search_user, name="search_user"),
	path("profile/<str:username>/", views.profile_page, name="profile"),
	# -------Samples/Uploads Links------------#
	path("upload/", views.upload, name="upload"),
	# path("sample/<int:sample_id>/", views.sample_player, name="sample_player"),
	# -------Posts Links------------#
	path("posts/", views.posts, name="posts"),
	path("user_post/<int:pk>", views.user_post, name="user_post"),
	# path('create_post/', views.create_post, name ='create_post'),
	path("create_post/", CreatePostView.as_view(), name="create_post"),
	path("update_post/<int:pk>", views.update_post, name="update_post"),
	path("delete_post/<int:pk>", views.delete_post, name="delete_post"),
	path("edit_profile/", views.edit_profile, name="edit_profile"),
	#Friend Requests:
	path('send-friend-request/<int:user_id>/', send_friend_request, name='send_friend_request'),
	path('accept-friend-request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
	path('decline-friend-request/<int:request_id>/', decline_friend_request, name='decline_friend_request'),
	path('remove-friend/<int:user_id>/', remove_friend, name='remove_friend'),  # URL for removing a friend


	#Chat stuff here
	path("chat/", views.recent_chat_redirect, name="recent_chat_redirect"),
	path("chat/<int:chat_id>/", views.chat, name="chat"),
	path('create_chat/', views.create_chat, name='create_chat'),
	path('chat/private/<int:user_id>/', views.private_chat_redirect, name='private_chat_redirect'),
	path('chat/delete/<int:chat_id>/', views.delete_chat, name='delete_chat'),
	path('send_message/<int:chat_id>/', views.add_message, name='send_message'),
	path('search_users/', views.search_users, name='search_users'), #To add users to auto-populating dropdown list

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
