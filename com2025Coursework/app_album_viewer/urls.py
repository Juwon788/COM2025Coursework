from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_album_viewer import views

urlpatterns = [
    path('welcome/', views.welcome, name ='welcome'),
    path('album_view/', views.album_view, name ='album_view'),
    path('add_album/', views.add_album, name ='add_album'),
    path('account/', views.account, name ='account'),
    path('delete_album//<int:album_id>/', views.delete_album, name ='delete_album'),
    path('edit_album//<int:album_id>/', views.edit_album, name ='edit_album'),
    path('album_detail/<int:album_id>/', views.album_detail, name ='album_detail'),
    path('album_detail/<int:album_id>/songs/', views.songs, name='songs'),
    path('album_detail/<int:album_id>/delete_songs/', views.delete_songs, name='delete_songs'),
    path('album_detail/<int:album_id>/add_songs/', views.add_songs, name='add_songs'),
    path('album_detail/<int:album_id>/comment/', views.comment, name='comment'),
    path('album_detail/<int:album_id>/recommend_friend', views.recommend_friend, name='recommend_friend'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
