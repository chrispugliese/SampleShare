from django.core.validators import FileExtensionValidator, ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import validators
from django.utils import timezone
from django.urls import reverse
from mutagen import mp3, wave

# Create your models here.

# ------User-Profiles---------------
# username = VARCHAR(50) NOT NULL
# dataOfBirth = VARCHAR(50) NOT NULL
# email = VARCHAR(50) NOT NULL
# password = VARCHAR(50) NOT NULL
# userPhote = TEXT NOT NULL
# bio = TEXT NOT NULL
# ------------------------------------
class UserProfile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	dateOfBirth = models.DateField()
	userPhoto = models.CharField(max_length=100)
	bio = models.TextField(max_length=1000)
	numberOfFollowers = models.IntegerField()
	friends = models.ManyToManyField('self', symmetrical=True, blank=True)
	def __str__(self):
		return str(self.user)

class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"


# ------Samples------
# samplename = VARCHAR(50) NOT NULL
# fileLocation = TEXT NOT NULL
# isPublic = BOOLEAN NOT NULL
# ------------------------------------
# TODO: need to ask if further validation is needed for file extensions
def validate_length(audio_file):
	max_length_allowed = 6.0
	audio = None
	if audio_file.name.endswith(".mp3"):
		audio = mp3.MP3(audio_file)
	elif audio_file.name.endswith(".wav"):
		audio = wave.WAVE(audio_file)

	if audio and audio.info.length > max_length_allowed + 0.9:
		raise ValidationError(
			"Only samples of 6 seconds length are allowed, please try another sample."
		)


class Sample(models.Model):
	sampleName = models.CharField(max_length=50)
	audioFile = models.FileField(
		upload_to="samples/",
		validators=[
			validate_length,
			FileExtensionValidator(allowed_extensions=["mp3", "wav"]),
		],
	)
	isPublic = models.BooleanField()
	# one to Many with UserProfiles
	userProfiles = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return f"{self.sampleName} {self.audioFile} {self.isPublic}"


# ------Chats------
# chatName = VARCHAR(50) NOT NULL
# chatTimeStamp = DATETIME NOT NULL
# ------------------------------------


class Chat(models.Model):
	chatName = models.CharField(max_length=50)
	chatTimeStamp = models.DateTimeField(auto_now_add=True)
	# Many to Many with UserProfiles
	userProfiles = models.ManyToManyField(UserProfile, null=True)

	def __str__(self):
		return f"{self.chatName} {self.chatTimeStamp}"


# ------Messages------
# message = TEXT NOT NULL
# messageTimeStamp = DATETIME NOT NULL
# ------------------------------------
class Message(models.Model):
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE)  # Linking to the Chat model
	user = models.ForeignKey(User, on_delete=models.CASCADE)  # Linking to the User model
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username}: {self.message[:20]} at {self.timestamp}"


# ------Genres------
# genrename = VARCHAR(50) NOT NULL
# ------------------------------------
class Genre(models.Model):
	genreName = models.CharField(max_length=50)
	# one to many with samples
	samples = models.ManyToManyField(Sample, null=True)

	def __str__(self):
		return f"{self.genreName}"


# ------Post------
# postText = VARCHAR(50) NOT NULL
# postTimeStamp = VARCHAR(50) NOT NULL
# ------------------------------------
class Post(models.Model):
	postText = models.TextField()
	postTimeStamp = models.DateTimeField(auto_now_add=True)
	# one to many with samples
	samples = models.ForeignKey(Sample, on_delete=models.CASCADE, null=True)
	# Many to Many with user-Profiles
	userProfiles = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return f"{self.postText} {self.postTimeStamp}"

	def get_absolute_url(self):
		return reverse("posts")


# ------Comments------
# commentMessage = TEXT NOT NULL
# commentTimeStamp = DATETIME NOT NULL
# ------------------------------------
class Comment(models.Model):
	commentMessage = models.TextField()
	commentTimeStamp = models.DateTimeField(auto_now_add=True)
	# One to Many with Posts
	posts = models.ForeignKey(Post, on_delete=models.CASCADE)
	# One to Many with Samples
	samples = models.ForeignKey(Sample, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return f"{self.commentMessage} {self.commentTimeStamp}"
