from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from .models import UserProfile, Sample
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm

# from playsound import playsound, PlaysoundException  # dont want this
import os


# Create your views here.
def home(request):
    return render(request, "home.html", {})


def user_detail(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)  # Query UserProfile by ID
    return render(request, "user_detail.html", {"user_profile": user_profile})


def page_not_found(request):
    raise Http404("Page not here tho")


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


# i dont like the playsound package, i will refactor this to use the html audio widget, maybe use js to make it cool.
def sample_player(request, sample_id):
    sample = get_object_or_404(Sample, id=sample_id)

    file_path_to_sample = sample.fileLocation
    try:
        if not os.path.exists(file_path_to_sample):
            raise FileNotFoundError(
                f"The sample file at {file_path_to_sample} does not exist."
            )

    except FileNotFoundError as fnf_error:
        message = f"File error: {fnf_error}"

    except Exception as e:
        message = f"An unexpected error has occurred: {e}"

    return render(request, "sample_player.html", {"sample": sample, "message": message})
