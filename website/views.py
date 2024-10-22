from django.conf import django, settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db.models import Q
from django.http import Http404, HttpRequest, StreamingHttpResponse, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView
from typing import AsyncGenerator
from .forms import SampleForm, SignUpForm, PostForm, MessageForm
from .models import Sample, UserProfile, Post, Chat, Message, FriendRequest
import asyncio, json, os


# Create your views here.
def home(request):
	profiles = UserProfile.objects.all()
	return render(request, "home.html", {})

def page_not_found(request):
	raise Http404("Page not here tho")


def profile_page(request, username):
	profile_user = get_object_or_404(User, username=username)
	is_owner = request.user == profile_user
	profile = get_object_or_404(UserProfile, user=profile_user)  # Query UserProfile by ID
	# Check if the logged-in user is a friend
	is_friend =  (
		request.user.userprofile.friends.filter(id=profile.id).exists() 
		if request.user.is_authenticated 
		else False
	)    
	# Check if there's a request already sent to viewed profile
	sent_request = (
		request.user.userprofile.sent_requests.filter(to_user=profile).first()
		if request.user.is_authenticated 
		else None
	)

	# Check if there's a friend request already sent from the viewed profile.
	received_request = (
		request.user.userprofile.received_requests.filter(from_user=profile).first()
		if request.user.is_authenticated
		else None
	)
	received_requests = FriendRequest.objects.filter(to_user=request.user.userprofile)

	context = {
		'profile': profile,
		'is_owner': is_owner,
		'is_friend': is_friend,
		'sent_request': sent_request,
		'received_request': received_request,
		'profile_user': profile_user,
		'received_requests': received_requests,
	}
	return render(request, 'profile_page.html', context)


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
			return render(request, "register.html", {"form": form})
	else:
		form = SignUpForm()
		return render(request, "register.html", {"form": form})

@login_required
def send_friend_request(request, user_id):
	to_user_profile = get_object_or_404(UserProfile, user_id=user_id)
	from_user_profile = get_object_or_404(UserProfile, user=request.user)
	#Doesn't create request if there's an existing one.
	if not FriendRequest.objects.filter(
		(Q(from_user=from_user_profile, to_user=to_user_profile) | 
		 Q(from_user=to_user_profile, to_user=from_user_profile))
	).exists():
		# Prevent sending a friend request to oneself
		if from_user_profile != to_user_profile:
			#Prevents sending if users are already friends
			if not from_user_profile.friends.filter(id=to_user_profile.id).exists():
				FriendRequest.objects.get_or_create(from_user=from_user_profile, to_user=to_user_profile)

	return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def accept_friend_request(request, request_id):
	friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user.userprofile)

	# Add each user to the other's friend list
	friend_request.from_user.friends.add(friend_request.to_user)
	friend_request.to_user.friends.add(friend_request.from_user)

	# Delete the friend request
	friend_request.delete()

	return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def decline_friend_request(request, request_id):
	 # Get the friend request and delete it
	friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user.userprofile)
	friend_request.delete()  # Simply delete the request

	return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_friend(request, user_id):
	friend_profile = get_object_or_404(UserProfile, user_id=user_id)
	user_profile = get_object_or_404(UserProfile, user=request.user)

	# Remove the friendship from both sides
	user_profile.friends.remove(friend_profile)
	friend_profile.friends.remove(user_profile)

	#return redirect('profile', username=friend_profile.user.username)
	return redirect(request.META.get('HTTP_REFERER', '/'))


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

#Used for auto-populating drop-down lists
def search_users(request):
	query = request.GET.get('query', '')
	users = User.objects.filter(username__icontains=query).exclude(username=request.user.username)  # Adjust filters as needed
	user_data = [{'username': user.username, 'avatar': staticfiles_storage.url(user.userprofile.userPhoto)} for user in users]
	return JsonResponse({'users': user_data})

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



def edit_profile(request):
	profile = request.user.userprofile
	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			# Handle file upload if a new file is uploaded
			if 'userPhoto' in request.FILES:
				# Save the file to a directory under 'media/profile_pics/'
				uploaded_file = request.FILES['userPhoto']
				file_path = os.path.join('profile_pics', uploaded_file.name)
				
				# Write the file to the media directory
				with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb+') as destination:
					for chunk in uploaded_file.chunks():
						destination.write(chunk)
				
				# Save the file path in the CharField
				profile.userPhoto = file_path

			# Save profile instance
			profile.save()
			return redirect('profile', username=request.user.username)
	else:
		form = ProfileForm(instance=profile)
	return render(request, 'edit_profile.html', {'form': form})
# --------------------------------------------------------------------#

#--------------------Start Chat code---------------------------
@login_required
def chat(request, chat_id):
	#Get the logged-in user from the session:
	user_profile = get_object_or_404(UserProfile, user=request.user)
	#Retrieves chat room by the room's ID
	chat = get_object_or_404(Chat, id=chat_id)

	# Check if the user is part of the chat's userProfiles (Many-to-Many)
	if user_profile not in chat.userProfiles.all():
		return redirect('home')  # Or show an error message

	chatMessages = chat.message_set.all().order_by('created_at')  # Get messages for the chat

	# Fetch all chats that the user is a part of (ordered by timestamp)
	user_chats = Chat.objects.filter(userProfiles=user_profile).order_by('-chatTimeStamp')

	return render(request, 'chat.html', {
		'chat': chat,        # Pass the chat room object
		'user_profile': user_profile,   # Pass the user profile
		'chats': user_chats,           # Pass the list of chats
		'chatMessages': chatMessages,           #Pass the sorted messages 
	})

def private_chat_redirect(request, user_id):
	# Get the logged-in user
	user_profile = get_object_or_404(UserProfile, user=request.user)
	# Get the profile user (the user whose profile is being visited)
	other_user = get_object_or_404(User, id=user_id)
	other_profile = get_object_or_404(UserProfile, user=other_user)

	# Check if the two users are friends
	if other_profile not in user_profile.friends.all():
		return redirect('home')  # Or show an error message (e.g., "You must be friends to chat")
	   #Incomplete- Should this send a chat request or just message them directly?

	# Check if a private chat between the two users already exists
	private_chat = Chat.objects.filter(
		userProfiles=user_profile
	).filter(
		userProfiles=other_profile, is_group_chat=False
	).first()

	if private_chat:
		# Redirect to the existing chat
		return redirect('chat', chat_id=private_chat.id)
	else:
		# If no chat exists, create a new private chat
		new_chat = create_chat(request, user_ids=[other_profile.user.id], is_group_chat=False, chat_name=None)
		if new_chat:
			return redirect('chat', chat_id=new_chat.id)
		else:
			return redirect('home')  # Handle the case where chat creation fails


@login_required
def create_chat(request):
	"""
	View to create a new chat. It can handle both private and group chats.
	:param user_ids: List of user IDs to include in the chat
	:param is_group_chat: Boolean flag to determine if it's a group chat
	:param chat_name: Optional name for group chats
	"""
	user_profile = get_object_or_404(UserProfile, user=request.user)

	if request.method == 'POST':
		chat_name = request.POST.get('chat_name')
		chat_usernames = request.POST.get('chat_users').split(',')  # Get the list of usernames from form
		other_users = UserProfile.objects.filter(user__username__in=chat_usernames)  # Fetch users by username

		if len(other_users) < 1:
			return None  # Handle the case where no users are provided (or raise an error)

		# Ensure the current user is included in the chat
		users = list(other_users) + [user_profile]

		# Determine if this is a group chat
		is_group_chat = len(users) > 2

		# Create the chat instance
		chat = Chat.objects.create(is_group_chat=is_group_chat)
		if is_group_chat:
			chat.chatName = chat_name  # Set the chat name for group chats

		# Add users to the chat
		chat.userProfiles.set(users)
		chat.save()

		return redirect('chat', chat_id=chat.id)  # Redirect after successful chat creation (adjust to your desired route)

	return render(request, 'create_chat.html')  # Render the form page in case of GET request

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
			return redirect('chat', chat_id=chat_id)  # Redirect to the chat page after posting
	else:
			# Form is invalid, render the chat page with errors
			messages.error(request, "There was an error with your submission.")  # Optional: Flash an error message
			messages = chat.message_set.all().order_by('created_at')  # Fetch messages for the chat
			return render(request, 'chat.html', {
				'chat': chat,
				'user_profile': request.user.userprofile,
				'chats': Chat.objects.filter(userProfiles=request.user.userprofile).order_by('-chatTimeStamp'),
				'chatMessages': chatMessages,
				'form': form,  # Pass the form back with errors
			})

	return redirect('chat', chat_id=chat_id)
#---------------------End chat Code------------------------------