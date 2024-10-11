from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
<<<<<<< Updated upstream
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
=======
from .models import Sample, UserProfile, Chat, Message, GroupChat, GroupMessage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

>>>>>>> Stashed changes

# Create your views here.
def home(request):

	profiles = UserProfile.objects.all()

	return render(request, 'home.html', {})

def user_detail(request, user_id):
	user_profile = get_object_or_404(UserProfile, id=user_id) #Query UserProfile by ID
	return render(request, 'user_detail.html', {'user_profile': user_profile})

def page_not_found(request):
	raise Http404("Page not here tho")

''' No longer in use?
def profile_page(request, pk):
<<<<<<< Updated upstream
    if request.user.is_authenticated:
        #Look up profiles
        user_profile = UserProfile.objects.get(id=pk)
        return render(request, 'profile_page.html', {'user_profile':user_profile})
    else:
        messages.success(request, "You must be logged in to view profiles")
        return redirect('home')


=======
	 if request.user.is_authenticated:
		 #Look up profiles
		 user_profile = UserProfile.objects.get(id=pk)
		 return render(request, 'profile_page.html', {'user_profile':user_profile})
	 else:
		messages.success(request, "You must be logged in to view profiles")
		return redirect('home')
'''


def profile_page(request, username):
	profile_user = get_object_or_404(User, username=username)

	is_owner = request.user == profile_user

	context = {
		'profile_user': profile_user,
		'is_owner': is_owner
	}

	return render(request, 'profile_page.html', context)

>>>>>>> Stashed changes


#Login/Logout/Register Users
def login_user(request):
	if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			#Authenticate
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, "Welcome back")
				return redirect('home')
			else: 
				messages.success(request, "Login information incorrect")
				return redirect('login')
	else:
		return render(request, 'login.html')

def logout_user(request):
	logout(request)
	messages.success(request, "Logged out")
	return redirect('home')

def register_user(request):
<<<<<<< Updated upstream
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate & log in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            date_of_birth = form.cleaned_data['date_of_birth']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Account Registered!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})
=======
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			#Authenticate & log in
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			date_of_birth = form.cleaned_data['date_of_birth']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "Account Registered!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})
	return render(request, 'register.html', {'form':form})

def search_user(request):
	if request.method == "GET":
		query = request.GET.get('q')  # 'q' is the name attribute in your search input field
		if query:
			matching_users = User.objects.filter(username__icontains=query)  # Case-insensitive search
			return render(request, 'search_results.html', {'users': matching_users, 'query': query})
		else:
			return render(request, 'search_results.html', {'users': None, 'query': query})
		
@login_required
def chat_view(request):
    chats = Chat.objects.all()  # Replace with your logic to get user's chats
    return render(request, 'chat.html', {'chats': chats})


@login_required
def create_chat(request):
	if request.method == 'POST':
		chat_name = request.POST.get('chat_name')
		chat = Chat.objects.create(chatName=chat_name, created_by=request.user)  # Set the created_by field
		chat.userProfiles.add(request.user.userprofile)
		return redirect('some_view_name')  # Redirect to a view after creating the chat (e.g., chat list)
	return render(request, 'create_chat.html')  # Render a template for creating a chat

@login_required
def create_group_chat(request):
	if request.method == 'POST':
		chat_name = request.POST.get('chat_name')
		members_usernames = request.POST.getlist('members')  # Expecting a list of usernames
		members = User.objects.filter(username__in=members_usernames)  # Get User objects
		group_chat = GroupChat.objects.create(chatName=chat_name, created_by=request.user)
		# Add members to the group chat
		for member in members:
			group_chat.members.add(member.userprofile)
		# Send invitations (optional)
		for member in members:
			GroupChatInvitation.objects.create(chat=group_chat, invited_user=member, invited_by=request.user)
		return redirect('some_view_name')  # Redirect to a view after creating the chat
	return render(request, 'create_group_chat.html')  # Render template for creating a group chat


@login_required
def send_group_message(request, group_chat_id):
	group_chat = get_object_or_404(GroupChat, id=group_chat_id)
	if request.method == 'POST':
		content = request.POST.get('message_content')
		message = GroupMessage.objects.create(group_chat=group_chat, sender=request.user, content=content)
		return redirect('group_chat_detail', group_chat_id=group_chat.id)  # Redirect to the group chat detail view

@login_required
def group_chat_detail(request, group_chat_id):
	group_chat = get_object_or_404(GroupChat, id=group_chat_id)
	messages = GroupMessage.objects.filter(group_chat=group_chat).order_by('-timestamp')  # Get messages for the chat
	return render(request, 'group_chat_detail.html', {'group_chat': group_chat, 'messages': messages})

>>>>>>> Stashed changes
