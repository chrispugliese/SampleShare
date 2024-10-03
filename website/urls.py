from django.urls import path
from . import views
from django.http import Http404

urlpatterns = [
    path('', views.home, name='home'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),  # Dynamic user page
    path('user/', views.page_not_found),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    #-------Posts Links------------#
    path('posts/', views.posts, name ='posts'),
    path('user_post/' , views.user_post, name = 'user_post'),
    path('create_post/', views.create_post, name ='create_post'),
    path('update_post/<int:pk>', views.update_post, name ='update_post'),
    path('delete_post/<int:pk>', views.create_post, name = 'update_post'),
]