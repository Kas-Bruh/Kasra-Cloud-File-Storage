from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from .navigator import Navigator
from django.dispatch import receiver
import json
import shutil
import os



class NavigatorModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data = models.TextField()

    def saveNavigatorHelper(self, navigator):
        serializedData = json.dumps(navigator.serialize())
        self.data = serializedData
        self.save()

    def loadNavigatorHelper(self):
        if self.data:
            data = json.loads(self.data)
            navigator = Navigator()
            navigator.deserialize(data)
            return navigator
        else:
            return Navigator()
        
    
def uploadedFilePath(instance, fileName):
    return os.path.join(instance.navigator.user.username, fileName)

class UserFiles(models.Model):
    navigator = models.ForeignKey(NavigatorModel, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to=uploadedFilePath)
    uploadedAt = models.DateTimeField(auto_now_add=True)
    fileName = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.fileName} uploaded on {self.uploadedAt}"
    
    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)
    
@receiver(pre_delete, sender=User)  
def deleteUserFileUploadPath(sender, instance, **kwargs):
    userFileUploadPath = os.path.join("media", instance.username)
    if os.path.exists(userFileUploadPath):
        shutil.rmtree(userFileUploadPath)