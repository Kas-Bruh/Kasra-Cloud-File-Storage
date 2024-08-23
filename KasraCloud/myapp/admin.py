from django.contrib import admin
from .models import NavigatorModel, UserFiles

@admin.register(NavigatorModel)
class NavigatorAdmin(admin.ModelAdmin):
    list_display = ("user",) 
    search_fields = ("user__username",)  

@admin.register(UserFiles)
class UserFilesAdmin(admin.ModelAdmin):
    list_display = ("navigator", "fileName", "uploadedAt")  
    search_fields = ("navigator__user__username", "fileName") 
    list_filter = ("uploadedAt",) 