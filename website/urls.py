from django.urls import path
from . import views
from django.http import Http404
from .views import create_chat, chat_view


urlpatterns = [
<<<<<<< Updated upstream
    path('', views.home, name='home'),
    path('profile/<int:pk>/', views.profile_page, name='profile'),  # Dynamic user page
    path('user/', views.page_not_found),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
=======
	path('', views.home, name='home'),
	path('profile/<str:username>/', views.profile_page, name='profile'),  # Dynamic user page
	path('user/', views.page_not_found),
	path('login/', views.login_user, name='login'),
	path('logout/', views.logout_user, name='logout'),
	path('register/', views.register_user, name='register'),
	path('search/', views.search_user, name='search_user'),
>>>>>>> Stashed changes

	#Chat Functionality:
	path('chat/', views.chat_view, name='chat'),
	path('create_chat/', views.create_chat, name='create_chat'),
	path('create_group_chat/', views.create_group_chat, name='create_group_chat'),
	path('group_chat/<int:group_chat_id>/', views.group_chat_detail, name='group_chat_detail'),
	path('group_chat/<int:group_chat_id>/send_message/', views.send_group_message, name='send_group_message'),
]