import json
import os
from django.core.management.base import BaseCommand
from django.db import connection
from django.core.exceptions import MultipleObjectsReturned
from app_album_viewer.models import UserDetails, Album, Song, Comment
from django.contrib.auth.hashers import make_password, check_password

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        print("Seeding the database..........\n")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        useduser = []
        useremail = []
        json_file_path = os.path.join(current_dir, 'sample_data.json')
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            for album_data in data['albums']:
                comments_data = album_data.pop('comments', [])
                album = Album.objects.create(**album_data)

                
                for comment_data in comments_data:
                    username = comment_data.get('user__display_name')
                    user = comment_data.get('user')
                    user_email = comment_data.get('user_email')
                    message = comment_data.get('message', '')
                    
                    if username is not None and username != "":
                        Comment.objects.create(
                                    album=album,
                                    message=message,
                                    user=username)

                        if username not in useduser:
                            useduser.append(username)
                    
                    if user_email is not None:
                        if user_email not in useremail:
                            useremail.append(user_email)
                            
                        
                    
                    
                    if user is not None and user != "":
                        Comment.objects.create(
                                    album=album,
                                    message=message,
                                    user=user)

                        if user not in useduser:
                            useduser.append(user)
                    
            #print(len(useremail))
            #print(len(useduser))
            for i in range(len(useduser)):
                UserDetails.objects.create(username=useduser[i], email=useremail[i], password=make_password('password'))

            for song_data in data['songs']:
                album_titles = song_data.pop('albums', [])
                song = Song.objects.create(**song_data)
                
                for title in album_titles:
                    try:
                        
                        album = Album.objects.get(title=title)
                        song.albums.add(album)
                    except MultipleObjectsReturned:
                        albums = Album.objects.filter(title=title)

                            

            

        print("Database has been seeded.")