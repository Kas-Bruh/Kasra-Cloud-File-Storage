from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.start, name='start'),        
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),    
    path('delete/', views.delete, name='delete'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('addFolder/', views.addFolder, name='addFolder'),
    path("addFile/", views.addFile, name="addFile"),
    path('enterFolder/', views.enterFolder, name='enterFolder'),
    path('navigateUp/', views.navigateUp, name='navigateUp'),
    path('search/', views.search, name='search'),
    path('rename/', views.rename, name='rename'),
    path('checkEverything/', views.checkEverything, name='checkEverything'),
    path('getFilePath/', views.getFilePath, name='getFilePath'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)