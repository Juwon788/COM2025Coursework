from django.test import TestCase, Client
from django.contrib.auth.hashers import check_password
from .forms import LoginForm, ContactsForm, UserSignUpForm, RecommendForm, CommentForm, AlbumForm
from app_album_viewer.models import UserDetails, Comment, Album
from django.contrib.auth.models import User
from django.urls import reverse
import re

# Create your tests here.
class TestLoginForm(TestCase): #Tests the login form

    def test_valid_login(self): # Test valid form data
        UserDetails.objects.create_user(
            email='annabaston@example.com',
            firstname='Anna',
            surname='Baston',
            username='AnnaB93',
            password='password'
        )
        form = {
            'username': 'AnnaB93',
            'password': 'password'
        }
        username = form['username']
        password = form['password']
        user = UserDetails.objects.get(username=username)
        user_valid = check_password(password, user.password)
        self.assertTrue(user_valid)
        

    def test_invalid_login(self): # Test invalid form data
        form_data = {
            'username': '', 
            'password': '' 
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

class UserSignUpFormTest(TestCase): #Tests the signup form
    def test_valid_form(self): #Tests for the valid signup form
        form_data = {
            'fullname': 'David Raya',
            'email': 'David@example.com',
            'username': 'davidraya',
            'password': 'password',
            'password1': 'password'
        }
        form = UserSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self): #Tests for the invalid signup form
        form_data = {
            'fullname': 'Smith',
            'email': 'wrongemail',
            'username': '', 
            'password': 'password',
            'password1': 'password123'
        }
        form = UserSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())


class RecommendFormTest(TestCase): #Tests the recommend form for the user
    def test_valid_form(self): #Tests for the recommend form (valid)
        form_data = {
            'email': 'recipient@example.com',
            'message': 'Hey, check out this album!',
            'subject': 'Music Recommendation'
        }
        form = RecommendForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self): #Tests when incorrect entries are entered
        form_data = {
            'email': 'invalid_email',
            'message': 'Hey, check out this album!',
            'subject': 'Music Recommendation'
        }
        email_verification = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        valid = False 
        email = form_data['email']
        if not re.match(email_verification, email):
            valid = False
        else:
            valid = True
        
        self.assertFalse(valid)

class TestCommentForm(TestCase): #Tests the comments
    def test_comment_form(self): #Tests the comment form and checks if it is in the table
        form_data = {'comment': 'Test comment.'}
        form = CommentForm(data=form_data)
        user = 'someguy'
        self.assertTrue(form.is_valid()) #Check if comment was added

        album = Album.objects.create( #Makes an album in the album table
            title='Test Album 1',
            description='Test Description 1',
            artist='Test Artist 1',
            price=10.99,
            format='Vinyl',
            release_date='2023-01-01'
        )

        Comment.objects.create( #Make a comment in the comment table
            album=album,
            user=user,
            message=form_data['comment'],
            )
        saved_comment = Comment.objects.get(user=user)
        self.assertEqual(saved_comment.message, 'Test comment.') #Checks if the added comment is in the file


class TestAlbumForm(TestCase): #Tests with the Add album form
    def test_valid_album_form(self): #Tests for valid inputs
        form_data = {
            'cover': 'album_cover.jpg',
            'title': 'Album Title',
            'description': 'Album description',
            'artist': 'Album Artist',
            'price': 9.99,
            'format': 'CD'
        }

        form = AlbumForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_album_form(self): #Tests for wrong album inputs
        form_data = {
            'cover': '', 
            'description': 'Album description',
            'artist': '',
            'price': 'Wrong Price',
            'format': '' 
        }

        form = AlbumForm(data=form_data)
        self.assertFalse(form.is_valid())



class TestContactsForm(TestCase):  #Tests the contact form
    def test_form_fields(self):
        form = ContactsForm()
        self.assertEqual(form.fields['email'].label, 'Enter your email')
        self.assertEqual(form.fields['message'].label, 'Enter your message')

    def test_valid_form(self): #Tests for valid contact data
        form_data = {
            'email': 'test@example.com',
            'message': 'This is a test message'
        }
        form = ContactsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self): #Tests for invalid contact data
        form_data = {
            'email': 'invalid_email',  
            'message': ''  
        }
        form = ContactsForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestAppPagesViews(TestCase): #Tests all the views
    def setUp(self): #This sets up the tests
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_home_view(self): #This tests the home page
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view(self): #This tests the contact page
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self): #This tests the login view page
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_view(self): #This tests the sign up page
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self): #This tests the about us page
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)