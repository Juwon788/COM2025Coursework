from django.db import models

# Create your models here.
class UserLogin(models.Model): #For the user sign in
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        managed = False

class UserSignUp(models.Model): #For the user sign up
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    password1 = models.CharField(max_length=100)

    class Meta:
        managed = False


class AddAlbum(models.Model): #This allows users to add to the album
    FORMAT_CHOICES = [
        ('CD', 'CD'),
        ('Vinyl', 'Vinyl'),
        ('Digital', 'Digital download'),
    ]
    cover = models.ImageField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    artist = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    format = models.CharField(max_length=50, choices=FORMAT_CHOICES)

    class Meta:
        managed = False

class Comment(models.Model):
    comment = models.CharField(max_length=100)

    class Meta:
        managed = False

class Recommend(models.Model):
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    class Meta:
        managed = False

class Contact(models.Model):
    email = models.CharField(max_length=100)
    message = models.TextField()

    class Meta:
        managed = False