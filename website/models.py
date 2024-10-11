from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

# ------User-Profiles---------------
# username = VARCHAR(50) NOT NULL
# dataOfBirth = VARCHAR(50) NOT NULL
# email = VARCHAR(50) NOT NULL
# password = VARCHAR(50) NOT NULL
# userPhote = TEXT NOT NULL
# bio = TEXT NOT NULL
#------------------------------------
class UserProfile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	dateOfBirth = models.DateField()
	userPhoto = models.CharField(max_length=100)
	bio = models.TextField(max_length=1000)
	numberOfFollowers = models.IntegerField()


	def __str__(self):
		return str(self.user)

# ------Samples------
# samplename = VARCHAR(50) NOT NULL
# fileLocation = TEXT NOT NULL
# isPublic = BOOLEAN NOT NULL
#------------------------------------
class Sample(models.Model):
	sampleName = models.CharField(max_length = 50)
	fileLocation = models.TextField()
	isPublic = models.BooleanField()
	# Many to Many with UserProfiles
	userProfiles = models.ManyToManyField(UserProfile, blank=True)
	def __str__(self):
		return(f"{self.sampleName} {self.fileLocation} {self.isPublic}")

# ------Genres------
# genrename = VARCHAR(50) NOT NULL
#------------------------------------
class Genre(models.Model):
	genreName = models.CharField(max_length = 50)
	# one to many with samples
	samples = models.ManyToManyField(Sample, blank=True)
	def __str__(self):
		return(f"{self.genreName}")









# ------Chats------
# chatName = VARCHAR(50) NOT NULL
# chatTimeStamp = DATETIME NOT NULL
#------------------------------------

class Chat(models.Model):
	chatName = models.CharField(max_length = 50)
	chatTimeStamp = models.DateTimeField(auto_now_add=True)
	is_group = models.BooleanField(default=False)  # Indicates if this is a group chat
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Track who created the chat
	# Many to Many with UserProfiles
	userProfiles = models.ManyToManyField(UserProfile, blank=True)
	def __str__(self):
		return(f"{self.chatName} {self.chatTimeStamp}")


# ------Messages------
# message = TEXT NOT NULL
# messageTimeStamp = DATETIME NOT NULL
#------------------------------------
class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	message = models.TextField()
	messageTimeStamp = models.DateTimeField(auto_now_add=True)
	# one to many with Chats
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
	def __str__(self):
		return(f"{self.message} {self.messageTimeStamp}")

#Creates invitations to invite users to join a group chat.
class GroupChatInvitation(models.Model):
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
	invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invited_user')
	invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invited_by')
	timestamp = models.DateTimeField(auto_now_add=True)
	accepted = models.BooleanField(default=False)
	def __str__(self):
		return f"Invitation to {self.invited_user.username} from {self.invited_by.username} for {self.chat.chatName}"

class GroupChat(models.Model):
	chatName = models.CharField(max_length=50)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	members = models.ManyToManyField(UserProfile, related_name='group_chats')  # Members of the group chat
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"GroupChat: {self.chatName}"


class GroupMessage(models.Model):
	group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Message from {self.sender.username} in {self.group_chat.chatName}"


#Separates unread messages from currently read messages
class UnreadMessage(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	message = models.ForeignKey(Message, on_delete=models.CASCADE)
	is_read = models.BooleanField(default=False)

	def __str__(self):
		return f"Unread message for {self.user.username} from {self.message.sender.username}"





# ------Post------
# postText = VARCHAR(50) NOT NULL
# postTimeStamp = VARCHAR(50) NOT NULL
#------------------------------------
class Post(models.Model):
	postText = models.TextField()
	postTimeStamp = models.DateTimeField(auto_now_add=True)
	# one to many with samples
	samples = models.ForeignKey(Sample, on_delete=models.CASCADE, null=True)
	# Many to Many with user-Profiles
	userProfiles = models.ManyToManyField(UserProfile, blank=True)

	def __str__(self):
		return(f"{self.postText} {self.postTimeStamp}")

# ------Comments------
# commentMessage = TEXT NOT NULL
# commentTimeStamp = DATETIME NOT NULL
#------------------------------------
class Comment(models.Model):
<<<<<<< Updated upstream
    commentMessage = models.TextField()
    commentTimeStamp = models.DateTimeField(auto_now_add=True)
    # One to Many with Posts
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    # One to Many with Samples
    samples = models.ForeignKey(Sample, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return(f"{self.commentMessage} {self.commentTimeStamp}")
=======
	commentMessage = models.TextField()
	commentTimeStamp = models.DateTimeField(auto_now_add=True)
	# One to Many with Posts
	posts = models.ForeignKey(Post, on_delete=models.CASCADE)
	# One to Many with Samples
	samples = models.ForeignKey(Sample, on_delete=models.CASCADE, null=True)
	def __str__(self):
		return(f"{self.commentMessage} {self.commentTimeStamp}")
	
>>>>>>> Stashed changes
