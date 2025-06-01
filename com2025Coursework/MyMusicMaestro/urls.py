from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [ #These are my urls
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name = 'base.html')),
    path('pages/', include('app_pages.urls')),
    path('album/', include('app_album_viewer.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
