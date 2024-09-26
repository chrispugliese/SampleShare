from django.db import models

# Create your models here.

# ------User-Profiles---------------
# username = VARCHAR(50) NOT NULL
# dataOfBirth = VARCHAR(50) NOT NULL
# email = VARCHAR(50) NOT NULL
# password = VARCHAR(50) NOT NULL
# userPhote = VARCHAR (50) NOT NULL
# bio = TEXT NOT NULL
#------------------------------------
class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    dateOfBirth = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    userPhoto = models.CharField(max_length=50)
    bio = models.TextField()
    numberOfFollowers = models.IntegerField()

# ------Samples------
# samplename = VARCHAR(50) NOT NULL
# fileLocation = VARCHAR(50) NOT NULL
# isPublic = BOOLEAN NOT NULL
#------------------------------------
class Sample(models.Model):
    sampleName = models.CharField(max_length = 50)
    fileLocation = models.CharField(max_length= 100)
    isPublic = models.BooleanField()
    # Many to Many with UserProfiles
    userProfiles = models.ManyToManyField(UserProfile)

class Chat(models.Model):
    chatName = models.CharField(max_length = 50)
    chatTimeStamp = models.DateTimeField(auto_new_add =True)

class Message(models.Model):
    message = models.TextField()
    messageTimeStamp = models.TextField()