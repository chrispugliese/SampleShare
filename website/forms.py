from django.utils.text import slugify
from django.core.exceptions import ValidationError
from mutagen import File as MutagenFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Sample, UserProfile, Post, Comment, Genre
import os, mimetypes


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ["sampleName", "audioFile", "isPublic", "userProfiles"]
        widgets = {
            "userProfiles": forms.HiddenInput(
                attrs={
                    "class": "form-control",
                    "id": "user",
                    "type": "hidden",
                }
            )
        }

    def clean_audioFile(self):
        file = self.cleaned_data.get("audioFile")

        if file:
            # Validate file size and type
            validate_audio_file(file)

            # Sanitize file name (remove dangerous characters and format the name)
            file.name = sanitize_filename(file.name)

        return file


def sanitize_filename(file_name):
    """
    This function removes any special characters from the filename and slugifies it.
    """
    base_name, extension = os.path.splitext(file_name)
    safe_name = slugify(
        base_name
    )  # Slugify the base name to remove unwanted characters
    return f"{safe_name}{extension}"


def validate_audio_file(file):
    allowed_extensions = ["mp3", "wav"]
    mime_type, _ = mimetypes.guess_type(file.name)

    if mime_type not in ["audio/mpeg", "audio/wav"]:
        raise ValidationError(
            "Invalid file type. Only .mp3 and .wav files are allowed."
        )

    # Validate file size (e.g., 10 MB limit)
    max_file_size = 10 * 1024 * 1024  # 10 MB
    if file.size > max_file_size:
        raise ValidationError("File size exceeds the limit of 10MB.")

    # Validate file content (ensure it's a valid audio file)
    try:
        audio = MutagenFile(file, easy=True)
        if audio is None:
            raise ValidationError("Invalid audio file content.")
    except Exception as e:
        raise ValidationError(f"Error processing audio file: {str(e)}")


class SampleEditForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ["sampleName", "isPublic", "userProfiles"]
        labels = {"isPublic": "Make Sample Public?"}
        widgets = {
            "userProfiles": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "value": "",
                    "id": "user",
                    "type": "hidden",
                }
            )
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        )
    )
    username = forms.CharField(
        max_length=25,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "YYYY-MM-DD",
            }
        )
    )

    class Meta:
        model = User
        fields = ("username", "email", "date_of_birth", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["username"].label = ""
        self.fields["username"].help_text = (
            '<span class="form-text text-muted"><small>Required. 25 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        )

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password1"].label = ""
        self.fields["password1"].help_text = (
            "<ul class=\"form-text text-muted small\"><li>Your password can't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can't be a commonly used password.</li><li>Your password can't be entirely numeric.</li></ul>"
        )

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["password2"].label = ""
        self.fields["password2"].help_text = (
            '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
        )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Save the UserProfile details
            date_of_birth = self.cleaned_data["date_of_birth"]
            # Create the associated UserProfile instance
            UserProfile.objects.create(
                user=user,
                dateOfBirth=date_of_birth,
                numberOfFollowers=0,  # default to 0
            )
        return user


# -----------------Post Form-----------------
class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop("user_id", None)
        super(PostForm, self).__init__(*args, **kwargs)
        if user_id is not None:
            self.fields["samples"].queryset = Sample.objects.filter(
                userProfiles=user_id
            )
        # else:
        # self.fields['samples'].queryset = Sample.objects.none()

    class Meta:
        model = Post
        fields = ("postText", "userProfiles", "samples")
        widgets = {
            "postText": forms.TextInput(attrs={"class": "form-control"}),
            #'userProfiles': forms.Select(attrs={'class': 'form-control'}),
            "userProfiles": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "value": "",
                    "id": "user",
                    "type": "hidden",
                }
            ),
            "samples": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }


# ---------------------------------------------------


class MessageForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Type message..."}),
        max_length=1000,
        required=True,
    )


# -------------------Profile Form--------------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "userPhoto"]


# ----------------------Comment Code------------------#\


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop("userProfile_id", None)
        super(CommentForm, self).__init__(*args, **kwargs)
        if user_id is not None:
            self.fields["samples"].queryset = Sample.objects.filter(
                userProfiles=user_id
            )

    class Meta:
        model = Comment
        fields = ("commentMessage", "posts", "samples", "userProfile")

        widgets = {
            "commentMessage": forms.TextInput(attrs={"class": "form-control"}),
            "posts": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "value": "",
                    "id": "post",
                    "type": "hidden",
                }
            ),
            "samples": forms.Select(attrs={"class": "form-control"}),
            "userProfile": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "value": "",
                    "id": "user",
                    "type": "hidden",
                }
            ),
        }


# ----------------------------------------------------#
