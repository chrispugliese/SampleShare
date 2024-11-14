from .views import CreateCommentView, send_friend_request, accept_friend_request, decline_friend_request, remove_friend, private_chat_redirect, get_received_requests_count
from django.urls import path
from . import views
from django.http import Http404
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("user/<int:user_id>/", views.user_detail, name="user_detail"),  # Dynamic user page
    path("user/", views.page_not_found),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("search/", views.search_user, name="search_user"),
    path("profile/<str:username>/", views.profile_page, name="profile"),
    path("delete-account/", views.delete_account, name="delete_account"),
    # -------Samples/Uploads Links------------#
    path("upload/", views.upload, name="upload"),
    path("edit_samples/", views.update_user_samples, name="edit_samples"),
    path("delete_user_sample/<int:sample_id>/", views.delete_user_sample, name="delete_user_sample",),
    path("sample/", views.sample_player, name="sample_player"),
    path('create-genres/', views.CreateGenreView.as_view(), name='create_genres'),
    path('search-genres/', views.search_genres, name='search_genres'),
    # -------Posts Links------------#
    #path("posts/", views.posts, name="posts"),
    path("user_post/<int:pk>", views.user_post, name="user_post"),
    # path('create_post/', views.create_post, name ='create_post'),
    path("create_post/<int:pk>", views.create_post, name="create_post"),
    path("update_post/<int:pk>", views.update_post, name="update_post"),
    path("delete_post/<int:pk>", views.delete_post, name="delete_post"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    # --------Comment Links--------------#
    path("create_comment/<int:pk>", views.create_comment, name="create_comment"),
    path("comments/<int:pk>", views.comments, name="comments"),
    path("comment_detail/<int:pk>", views.comment_detail, name="comment_detail"),
    path("update_comment/<int:pk>", views.update_comment, name="update_comment"),
    path("delete_comment/<int:pk>", views.delete_comment, name="delete_comment"),
    path("like/<int:pk>", views.like_view, name='like_post'),
    # --------------------------------------#
    
    #Friend Requests:
	path('send-friend-request/<int:user_id>/', send_friend_request, name='send_friend_request'),
	path('accept-friend-request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
	path('decline-friend-request/<int:request_id>/', decline_friend_request, name='decline_friend_request'),
	path('remove-friend/<int:user_id>/', remove_friend, name='remove_friend'),  # URL for removing a friend

    path('get_received_requests_count/', get_received_requests_count, name='get_received_requests_count'),

	#Chat stuff here
	path("chat/", views.recent_chat_redirect, name="recent_chat_redirect"),
	path("chat/<int:chat_id>/", views.chat, name="chat"),
	path('create_chat/', views.create_chat, name='create_chat'),
	path('chat/private/<int:user_id>/', views.private_chat_redirect, name='private_chat_redirect'),
	path('chat/delete/<int:chat_id>/', views.delete_chat, name='delete_chat'),
	path('send_message/<int:chat_id>/', views.add_message, name='send_message'),
	path('search_users/', views.search_users, name='search_users'), #To add users to auto-populating dropdown list

    #---------------download url--------------------#
    path('download/<int:pk>', views.download_sample , name="download_sample"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
