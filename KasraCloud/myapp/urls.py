from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.start, name='start'),        # Root URL points to start view
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),     # Home URL points to home view
    path('delete/', views.delete, name='delete'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('addFolder/', views.addFolder, name='addFolder'),
    path("addFile/", views.addFile, name="addFile"),
    path('enterFolder/', views.enterFolder, name='enterFolder'),
    path('navigateUp/', views.navigateUp, name='navigateUp'),
    path('search/', views.search, name='search'),
    path('rename/', views.rename, name='rename'),
    path('checkEverything/', views.checkEverything, name='checkEverything'),
    path('delete/', views.delete, name='delete'),
    path('getFilePath/', views.getFilePath, name='getFilePath'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)