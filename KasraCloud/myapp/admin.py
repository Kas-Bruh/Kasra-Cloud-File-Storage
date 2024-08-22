from django.contrib import admin
from .models import NavigatorModel, UserFiles

@admin.register(NavigatorModel)
class NavigatorAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Display the user associated with the NavigatorModel
    search_fields = ('user__username',)  # Allow searching by username

@admin.register(UserFiles)
class UserFilesAdmin(admin.ModelAdmin):
    list_display = ('navigator', 'fileName', 'uploaded_at')  # Customize columns in the admin list view
    search_fields = ('navigator__user__username', 'fileName')  # Allow searching by username and file name
    list_filter = ('uploaded_at',)  # Filter by upload date