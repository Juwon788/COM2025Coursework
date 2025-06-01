from django.contrib import admin
from .models import *
from app_album_viewer.models import UserDetails

# Register your models here.
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Comment)
admin.site.register(UserDetails)