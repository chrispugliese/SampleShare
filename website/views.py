from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Sample, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm 
from django.contrib.auth.models import User


# Create your views here.
def home(request):

    profiles = UserProfile.objects.all()

    return render(request, 'home.html', {})

def user_detail(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id) #Query UserProfile by ID
    return render(request, 'user_detail.html', {'user_profile': user_profile})

def page_not_found(request):
    raise Http404("Page not here tho")


def profile_page(request, pk):
    if request.user.is_authenticated:
        # Look up the User first
        user = get_object_or_404(User, pk=pk)
        # Then look up the UserProfile associated with that User
        user_profile = get_object_or_404(UserProfile, user=user)
        return render(request, 'profile_page.html', {'user_profile': user_profile})
    else:
        messages.success(request, "You must be logged in to view profiles")
        return redirect('home')




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
        
        
        