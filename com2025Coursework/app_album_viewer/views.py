from django.shortcuts import render, redirect
from django.http import HttpResponse
from app_pages.forms import AlbumForm, CommentForm, RecommendForm
from app_album_viewer.models import Album, Song, Comment, UserDetails
import re, os
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.http import JsonResponse


def welcome(request): #This is the welcome page after logging in
    image_url = '/media/dripping-stereo.png'
    username = request.session['username']

    return render(request, 'welcomepage.html', {'image_url': image_url, 'username': username})



# Create your views here.
def album_view(request): #This shows the albums on the website
    albums = Album.objects.all()
    songs = Song.objects.all()
    comments = Comment.objects.all()
    return render(request, 'album_view.html', {'albums': albums, 'songs': songs, 'comments': comments})


def add_album(request):
    form = AlbumForm()
    show_button = request.session.get('show_button', True)  # Fetch show_button value from session

    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            cover = form.cleaned_data['cover']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            artist = form.cleaned_data['artist']
            price = form.cleaned_data['price']
            format = form.cleaned_data['format']
            current_date = datetime.now().date()
            release_date = current_date.strftime("%Y-%m-%d")

            if not all([title, description, artist, price, format]):
                error_message = "Please fill in all the fields."
                return render(request, 'add_album.html', {'form': form, 'error_message': error_message, 'show_button': show_button})
            elif price < 0:
                error_message = "Enter a valid price"
                return render(request, 'add_album.html', {'form': form, 'error_message': error_message, 'show_button': show_button})
            else:
                if cover is not None:
                    handle_uploaded_file(cover)
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                    covername = fs.save(cover.name, cover)
                else:
                    covername = 'default.png'

                new_album = Album.objects.create(
                    cover=covername,
                    title=title,
                    description=description,
                    artist=artist,
                    price=price,
                    format=format,
                    release_date=release_date
                )
                message = "You have created album " + title
                show_button = False  # Set show_button to False after successful album creation
                request.session['show_button'] = show_button  # Update the session value
                return render(request, 'add_album.html', {'message': message, 'show_button': show_button})
    show_button = True
    return render(request, 'add_album.html', {'form': form, 'show_button': show_button})

def handle_uploaded_file(file):
    with open(os.path.join('media', file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def album_detail(request, album_id): #This shows the albums
    album = get_object_or_404(Album, id=album_id)
    comments = Comment.objects.filter(id=album_id)

    return render(request, 'album_detail.html', {'album': album, 'comments': comments})


def delete_album(request, album_id): #This deletes the album
    album = get_object_or_404(Album, id=album_id)

    songs = Song.objects.filter(id=album_id)
    comments = Comment.objects.filter(album=album_id)

    songs.delete()
    comments.delete()
    album.delete()

    return redirect('/album/album_view')


def edit_album(request, album_id): #This allows the user to edit an album
    album = get_object_or_404(Album, id=album_id)
    
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            price = form.cleaned_data['price']
            if price < 0:
                error_message = "Enter a valid price"
                return render(request, 'edit_album.html', {'form': form, 'album': album, 'error_message': error_message})
            
            if 'cover' in form.changed_data: 
                cover = form.cleaned_data['cover']
                if cover:
                    handle_uploaded_file(cover)
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                    covername = fs.save(cover.name, cover)
                    album.cover = covername
            form.save()
            return redirect('/album/album_view')
    else:
        form = AlbumForm(instance=album)
    
    return render(request, 'edit_album.html', {'form': form, 'album': album})

def songs(request, album_id): #This shows the songs that are in an album
    album = Album.objects.get(pk=album_id)
    songs = Song.objects.filter(id=album_id)
    all_songs = Song.objects.all()
    return render(request, 'songs.html', {'songs': songs, 'album': album, 'all_songs': all_songs})

def delete_songs(request, album_id): #This allows to user to delete songs from an album
    album = get_object_or_404(Album, pk=album_id)
    if request.method == 'POST':
        song_ids_to_delete = request.POST.getlist('songs_to_delete')
        for song_id in song_ids_to_delete:
            song = get_object_or_404(Song, pk=song_id)
            song.delete()
        
        return redirect('songs', album_id=album_id)
    else:
        return redirect('songs', album_id=album_id)


def add_songs(request, album_id): #This allows the user to add songs to an album
    album = get_object_or_404(Album, pk=album_id)
    if request.method == 'POST':
        song_ids_to_add = request.POST.getlist('songs_to_add')
        for song_id in song_ids_to_add:
            song = get_object_or_404(Song, pk=song_id)
            album.songs.add(song) 

        return redirect('songs', album_id=album_id)
    
    else:
        return redirect('songs', album_id=album_id)

def comment(request, album_id): #This allows the user to comment on an album
    album = get_object_or_404(Album, pk=album_id)
    
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            username = request.session['username']  
            comment = form.cleaned_data['comment'] 
            Comment.objects.create(message=comment,
                                    album_id=album_id,
                                    user=username)
            form = CommentForm()
            message = "Message added successfully"
            return render(request, 'album_detail.html', {'form': form, 'album': album, 'message': message})

    else:  
        print(album)
        return render(request, 'comment.html', {'form': form, 'album': album})


def account(request): # This shows the user their comments  
    username = request.session['username'] 
    comments = Comment.objects.filter(user=username)
    return render(request, 'account.html', {'comments': comments})

def recommend_friend(request, album_id): #This allows the user to recommend an album to someone
    album = get_object_or_404(Album, pk=album_id)
    username = request.session['username']
    initial_message = _('RecommendTitle') % {'title': album.title, 'username': username}
    subject = "Music"
    initial_subject = _('subject') % {'subject': subject}
    initial_data = {"message": str(initial_message),
                    "subject": str(initial_subject)}
    form = RecommendForm(initial=initial_data)
    user_details = UserDetails.objects.get(username=username)
    from_email = user_details.email
    if request.method == 'POST':
        form = RecommendForm(request.POST)
        
        if form.is_valid():
            
            to_email = form.cleaned_data['email']
            email_verification = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_verification, to_email):
                error_message = "Email is invalid"
                success_message = ""
                return render(request, 'recommend_friend.html', {'form': form, 'album': album, 'error_message': error_message, 'success_message': success_message})

            message = form.cleaned_data['message']
            subject = form.cleaned_data['subject']
            form = RecommendForm()
            send_mail(subject, message, from_email, [to_email])
            success_message = "Email successfully sent"
            return render(request, 'recommend_friend.html', {'form': form, 'album': album, 'message': message, 'success_message': success_message})

    else:  
        return render(request, 'recommend_friend.html', {'form': form, 'album': album})
