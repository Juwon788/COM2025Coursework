from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UserSignUp, AddAlbum, Comment, Recommend, Contact

class LoginForm(AuthenticationForm): #This is the login form
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput()) #This prevents the password from being seen



class UserSignUpForm(forms.ModelForm): #The signup form
    class Meta:
        model = UserSignUp
        fields = ['fullname', 'email', 'username', 'password', 'password1']
        managed = False


    def __init__(self, *args, **kwargs): # These are the label names
        super().__init__(*args, **kwargs)
        self.fields['fullname'].label = 'Your fullname (First and Last names)'
        self.fields['email'].label = 'Your email'
        self.fields['username'].label = 'Your username'
        self.fields['password'].label = 'Your password'
        self.fields['password1'].label = 'Re-enter password'

class AlbumForm(forms.ModelForm): #The albums form form adding and edditing albums
    class Meta:
        model = AddAlbum
        fields = ['cover', 'title', 'description', 'artist', 'price', 'format']
        managed = False

    def __init__(self, *args, **kwargs): #Field names
        super().__init__(*args, **kwargs)
        self.fields['cover'].label = 'Enter your cover'
        self.fields['title'].label = 'Enter your title'
        self.fields['description'].label = 'Enter the description'
        self.fields['artist'].label = 'Enter the artist'
        self.fields['price'].label = 'Enter your price'
        self.fields['format'].label = 'Enter your format'

class CommentForm(forms.ModelForm): #The comments form
    class Meta:
        model = Comment
        fields = ['comment']
        managed = False

class RecommendForm(forms.ModelForm): #The reccomend form
    class Meta:
        model = Recommend
        fields = ['email', 'message', 'subject']
        managed = False

    def __init__(self, *args, **kwargs): #The names of the labels
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email of receipient'
        self.fields['message'].label = 'Enter your message'

class ContactsForm(forms.ModelForm): #Contacts form
    class Meta:
        model = Contact
        fields = ['email', 'message']
        managed = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Enter your email'
        self.fields['message'].label = 'Enter your message'

