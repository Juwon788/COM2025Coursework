from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_pages import views
from django.views.generic import TemplateView

urlpatterns = [ #These are my urls
    path('', TemplateView.as_view(template_name = 'welcomepage.html')),
    path('home/', views.home, name ='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.login, name ='login'),
    path('signup/', views.signup, name ='signup'),
    path('contact/', views.contact, name ='contact'),
    path('about/', views.about, name ='about'),
    
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
