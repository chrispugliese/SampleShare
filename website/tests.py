from django.test import TestCase, Client
from .models import *
from django.urls import reverse

# Create your tests here.
#This is testing that the samples table in the DB is able to store samples and retreive them
class SampleTestCase(TestCase):
    def setUp(self):
        self.my_object = Sample.objects.create(sampleName="Test Sample", audioFile="test.mp3", isPublic=False)

    def test_object_creation(self):
        self.assertEqual(self.my_object.sampleName, "Test Sample")

    def test_object_retrieval(self):
        obj = Sample.objects.get(sampleName = "Test Sample")
        self.assertEqual(obj, self.my_object)

# Testing to see if the posts table in the DB can store a post and be able to retrieve that data
class PostTestCase(TestCase):
    def setUp(self):
        self.my_object = Post.objects.create(postText="Test Post")

    def test_object_creation(self):
        self.assertEqual(self.my_object.postText, "Test Post")

    def test_object_retrieval(self):
        obj = Post.objects.get(postText = "Test Post")
        self.assertEqual(obj, self.my_object)

# Testing to see if creating a comment tied to the post is being store and retrieved correctly
class CommentTestCase(TestCase):
    def setUp(self):
        testPost = Post.objects.create(postText="Test Post")
        self.my_object = Comment.objects.create(commentMessage="Test Comment", posts=testPost)

    def test_object_creation(self):
        self.assertEqual(self.my_object.commentMessage, "Test Comment")

    def test_object_retrieval(self):
        obj = Comment.objects.get(commentMessage = "Test Comment")
        self.assertEqual(obj, self.my_object)

class UserProfileAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.userprofile
    