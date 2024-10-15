from django.conf import django
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, StreamingHttpResponse, HttpResponse
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from typing import AsyncGenerator
from .models import Sample, UserProfile, Post, Chat, Message, FriendRequest
from .forms import SampleForm, SignUpForm, PostForm, MessageForm
import asyncio, os, json 


# Create your views here.
def home(request):
<<<<<<< Updated upstream
	profiles = UserProfile.objects.all()
	return render(request, "home.html", {})
=======
    profiles = UserProfile.objects.all()
    return render(request, "home.html", {})
>>>>>>> Stashed changes

def page_not_found(request):
	raise Http404("Page not here tho")

@login_required
def profile_page(request, username):
<<<<<<< Updated upstream
	user = get_object_or_404(User, username=username)
	is_owner = request.user == user
	profile = get_object_or_404(UserProfile, user=user)  # Query UserProfile by ID
	# Check if the logged-in user is a friend
	is_friend =  (
		request.user.userprofile.friends.filter(id=profile.id).exists() 
		if request.user.is_authenticated 
		else False
	)
	# Check if there's a sent request
	sent_request = (
		request.user.userprofile.sent_requests.filter(to_user=profile).exists() 
		if request.user.is_authenticated 
		else False
	)
	# Check if there's a received request
	received_request = (
		user_profile.received_requests.filter(from_user=request.user.userprofile).exists()
		if request.user.is_authenticated
		else False
	)
	context = {
		'profile': profile,
		'is_owner': is_owner,
		'is_friend': is_friend,
		'sent_request': sent_request,
		'received_request': received_request,
	}
	print(f'Profile User ID: {profile.user.id if profile.user else "No user"}')
	return render(request, 'profile.html', context)
=======
    user = get_object_or_404(User, username=username)
    is_owner = request.user == user

    context = {"user": user, "is_owner": is_owner}

    return render(request, "profile_page.html", context)

>>>>>>> Stashed changes

# Login/Logout/Register Users
def login_user(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "Welcome back")
			return redirect("home")
		else:
			messages.success(request, "Login information incorrect")
			return redirect("login")
	else:
		return render(request, "login.html")


def logout_user(request):
	logout(request)
	messages.success(request, "Logged out")
	return redirect("home")


def register_user(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate & log in
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password1"]
			date_of_birth = form.cleaned_data["date_of_birth"]
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "Account Registered!")
			return redirect("home")
	else:
		form = SignUpForm()
		return render(request, "register.html", {"form": form})
	return render(request, "register.html", {"form": form})

@login_required
def send_friend_request(request, user_id):
	to_user_profile = get_object_or_404(UserProfile, user_id=user_id)
	from_user_profile = get_object_or_404(UserProfile, user=request.user)

	# Prevent sending a friend request to oneself
	if from_user_profile != to_user_profile:
		FriendRequest.objects.get_or_create(from_user=from_user_profile, to_user=to_user_profile)

	return redirect('profile', user_id=user_id)

@login_required
def accept_friend_request(request, request_id):
	friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user.userprofile)

	# Add each user to the other's friend list
	friend_request.from_user.friends.add(friend_request.to_user)
	friend_request.to_user.friends.add(friend_request.from_user)

	# Delete the friend request
	friend_request.delete()

	return redirect('profile', user_id=friend_request.from_user.user.id)

@login_required
def decline_friend_request(request, request_id):
	 # Get the friend request and delete it
	friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user.userprofile)
	friend_request.delete()  # Simply delete the request

	return redirect('profile', user_id=friend_request.from_user.user.id)

@login_required
def remove_friend(request, user_id):
	friend_profile = get_object_or_404(UserProfile, user__id=user_id)
	user_profile = get_object_or_404(UserProfile, user=request.user)

	# Remove the friendship from both sides
	user_profile.friends.remove(friend_profile)
	friend_profile.friends.remove(user_profile)

	return redirect('profile', user_id=user_id)



# TODO: need to add a 6 second restriction for audio files.
# and some exception handling for if user is logged or not.
def upload(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			form = SampleForm(request.POST, request.FILES or None)
			if form.is_valid():
				form.save()
				messages.success(request, "Your sample was uploaded successfully!")
				return redirect("home")
		else:
			form = SampleForm()
		return render(request, "upload.html", {"form": form})
	else:
		messages.error(request, "You must be logged in to upload a sample file!")
		return redirect("login")


def search_user(request):
	if request.method == "GET":
		query = request.GET.get(
			"q"
		)  # 'q' is the name attribute in your search input field
		if query:
			matching_users = User.objects.filter(
				username__icontains=query
			)  # Case-insensitive search
			return render(
				request,
				"search_results.html",
				{"users": matching_users, "query": query},
			)
		else:
			return render(
				request, "search_results.html", {"users": None, "query": query}
			)


# ----------------------------Post Code -------------------------------#
def posts(request):
	if request.user.is_authenticated:
		# Look Up Posts
		userPosts = Post.objects.all()
		return render(request, "posts.html", {"userPosts": userPosts})
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect("home")


def user_post(request, pk):
	if request.user.is_authenticated:
		user_post = Post.objects.get(id=pk)
		return render(request, "userPost.html", {"user_post": user_post})
	else:
		messages.success(request, "Your Must Be Logged In...")
		return redirect("home")


class CreatePostView(CreateView):
	model = Post
	form_class = PostForm
	template_name = "create_post.html"
	# fields = '__all__'


def update_post(request, pk):

	if request.user.is_authenticated:
		current_post = Post.objects.get(id=pk)
		form = PostForm(request.POST or None, instance=current_post)
		if request.method == "POST":
			if form.is_valid():
				add_post = form.save()
				messages.success(request, "Post Updated...")
				return redirect("home")
		return render(request, "update_post.html", {"form": form})
	else:
		messages.success(request, "Your Must Be Logged In...")
		return redirect("home")


def delete_post(request, pk):
	if request.user.is_authenticated:
		deletePost = Post.objects.get(id=pk)
		deletePost.delete()
		messages.success(request, "Post Was Deleted...")
		return redirect("posts")
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect("posts")


# --------------------------------------------------------------------#



#--------------------Start Chat code---------------------------
def chat(request, chat_id):
	# If the current user is not authenticated, redirect to the login page
	if not request.user.is_authenticated:
		return redirect('login_user')

	#Get the logged-in user from the session:
	user_profile = get_object_or_404(UserProfile, user=request.user)

	#Retrieves chat room by the room's ID
	chat_room = get_object_or_404(Chat, id=chat_id)

	# Check if the user is part of the chat's userProfiles (Many-to-Many)
	if user_profile not in chat_room.userProfiles.all():
		return redirect('home')  # Or show an error message

	messages = Message.objects.filter(chat=chat_room).order_by('-created_at')  # Get messages for the chat

	# Fetch all chats that the user is a part of (ordered by timestamp)
	user_chats = Chat.objects.filter(userProfiles=user_profile).order_by('-chatTimeStamp')

	return render(request, 'chat.html', {
		'chat_room': chat_room,        # Pass the chat room object
		'user_profile': user_profile,   # Pass the user profile
		'chats': user_chats,           # Pass the list of chats
		'messages': messages,           #Pass the sorted messages 
	})

@login_required  # Ensure user is logged in
def add_message(request, chat_id):
	chat = get_object_or_404(Chat, id=chat_id)  # Retrieve the chat instance

	if request.method == 'POST':
		form = MessageForm(request.POST)
		if form.is_valid():
			content = form.cleaned_data['content']
			# Create the new message instance
			Message.objects.create(chat=chat, user=request.user, content=content)
			chat.chatTimeStamp = timezone.now()
			chat.save()
			return redirect('chat', chat_id=chat.id)  # Redirect to the chat page after posting
	else:
		form = MessageForm()  # Create an empty form

	return render(request, 'chat.html', {'form': form, 'chat': chat})
#---------------------End chat Code------------------------------