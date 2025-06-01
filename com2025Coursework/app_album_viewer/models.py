from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class Album(models.Model): #Table for albums
    cover = models.ImageField(upload_to='', max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    artist = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    format = models.CharField(max_length=50)
    release_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.cover:
            self.cover = 'default.png'
        super(Album, self).save(*args, **kwargs)
    
class Song(models.Model): #Table for songs
    title = models.CharField(max_length=100)
    runtime = models.IntegerField()
    albums = models.ManyToManyField(Album, related_name='songs')


class UserDetailsManager(BaseUserManager): #The table for the custom user details
    def create_user(self, email, firstname, surname, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            surname=surname,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, surname, username, password):
        user = self.create_user(
            email=email,
            firstname=firstname,
            surname=surname,
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserDetails(AbstractBaseUser): #The table for the user's details
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    objects = UserDetailsManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'surname', 'username']

    def __str__(self):
        return self.email


class Comment(models.Model): #The table for the user comments
    album = models.ForeignKey(Album, related_name='comments', on_delete=models.CASCADE)
    user = models.CharField(max_length=50)
    message = models.CharField(max_length=100)




