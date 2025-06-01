from django.test import TestCase, Client
from .models import Album, Song, Comment, UserDetails
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.urls import reverse


# Create your tests here.

class AlbumModelTestCase(TestCase): #This tests if the album table has been constructed properly
    def setUp(self):
        self.album1 = Album.objects.create(   #Creates first album
            title="Test Album 1",
            description="Description for Test Album 1",
            artist="Test Artist 1",
            price=9.99,
            format="CD",
            release_date="2023-01-01"
        )
        self.album2 = Album.objects.create( #Creates album with a default.png file
            title="Test Album 2",
            description="Description for Test Album 2",
            artist="Test Artist 2",
            price=14.99,
            format="Vinyl",
            release_date="2022-05-15",
            cover="dripping-stereo.png"  
        )

    def test_default_cover(self):
        default_album = Album.objects.create( #Tests the default cover
            title="Default Cover Album",
            description="Description for Default Cover Album",
            artist="Default Artist",
            price=19.99,
            format="Digital",
            release_date="2022-12-31"
        )
        self.assertEqual(default_album.cover, 'default.png')

    def test_cover_assignment(self):  #Tests the regular and the default cover
        self.assertEqual(self.album1.cover, 'default.png')
        self.assertEqual(self.album2.cover, 'dripping-stereo.png')

    def test_string_representation(self): #Tests the titles of the table
        self.assertEqual(self.album1.title, "Test Album 1")
        self.assertEqual(self.album2.title, "Test Album 2")


class SongModelTestCase(TestCase): #Test case for the song table
    def setUp(self):
        self.song1 = Song.objects.create(   #Creates first song
            title = "Song title 1",
            runtime = 1000
        )
        self.song2 = Song.objects.create(   #Creates second song
            title = "Song title 2",
            runtime = 600
        )

    def test_title(self):  #Tests the titles
        self.assertEqual(self.song1.title, 'Song title 1')
        self.assertEqual(self.song2.title, 'Song title 2')


    def test_runtime(self):  #Tests the runtime
        self.assertEqual(self.song1.runtime, 1000)
        self.assertEqual(self.song2.runtime, 600)


class UserModelTestCase(TestCase): #Test case for the userdetails table
    def setUp(self):
        self.user = UserDetails.objects.create( #A user is created
            email='test@example.com',
            firstname='Dave',
            surname='Doe',
            username='davedoe',
            password='password'
        )

    def test_user_creation(self): #Checks if the user was added successfully
        self.assertEqual(UserDetails.objects.count(), 1)

    def test_unique_email(self): #Check if users have the same email (should fail)
        with self.assertRaises(Exception):
            UserDetails.objects.create(
                email='test@example.com',
                firstname='Alice',
                surname='Smith',
                username='alicesmith',
                password='password'
            )
    
    def test_string_representation(self): #Checks the email
        self.assertEqual(self.user.email, 'test@example.com')

    def test_user_authentication(self): #Test when the user enters correct credentials
        user = UserDetails.objects.get(username='davedoe')
        hashed_password = make_password('password') 
        password_matched = check_password(user.password, hashed_password)
        self.assertTrue(password_matched)

    def test_user_authentication_wrong(self): #Test when the user enters incorrect credentials
        user = UserDetails.objects.get(username='davedoe')
        hashed_password = make_password('hello') 
        password_matched = check_password(user.password, hashed_password)
        self.assertFalse(password_matched)


@classmethod
class CommentModelTest(TestCase):
    def setUpTestData(cls):
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
            user='Test User',
            message='This is a test comment.'
        )

    def test_comment_content(self):
        comment = Comment.objects.get(id=1)
        expected_album = Album.objects.get(id=1)
        self.assertEqual(comment.album, expected_album)
        self.assertEqual(comment.user, 'Test User')
        self.assertEqual(comment.message, 'This is a test comment.')

class TestAppAlbumViewerViews(TestCase): #Tests all the views
    def setUp(self): #This sets up the test
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_welcome_view(self): #Tests welcome page
        response = self.client.get('/welcome/')
        self.assertEqual(response.status_code, 404)
        # Add more assertions as needed

    def test_album_view(self): #Tests album_view
        response = self.client.get('/album/album_view/')
        self.assertEqual(response.status_code, 200)

    def test_recommend_friend_view(self): #Tests the recommend a friend view
        post_data = {
            'email': 'test@example.com',
            'message': 'Test message',
            'subject': 'Test subject'
        }
        response = self.client.post(reverse('recommend_friend', kwargs={'album_id': 1}), post_data)
        self.assertEqual(response.status_code, 404)

    def test_comment_view(self): #This tests the comments view
        self.client.login(username='testuser', password='testpassword')

        album = Album.objects.create(title="Test Album", description="Test description", artist="Test Artist", price=9.99, release_date="2023-06-06")
        comment_text = 'This is a test comment'

        session = self.client.session
        session['username'] = 'testuser' #creates the testuser
        session.save()

        url = reverse('comment', args=[album.id])
        response = self.client.post(url, {'comment': comment_text})

        self.assertEqual(response.status_code, 200)
        
        comments = Comment.objects.filter(album=album, message=comment_text)
        self.assertTrue(comments.exists())

    def test_album_detail_view(self): # Tests the album_detail view
        
        album = Album.objects.create(title="Test Album", description="Test description", artist="Test Artist", price=9.99, release_date="2023-06-06")
        response = self.client.get(reverse('album_detail', args=[album.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'album_detail.html')

    def test_invalid_album_detail_view(self): #Test for my invalid album details
        response = self.client.get(reverse('album_detail', args=[1000])) #Enters an invalid album id
        self.assertEqual(response.status_code, 404)