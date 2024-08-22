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
        serialized_data = json.dumps(navigator.serialize())
        self.data = serialized_data
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
    navigator = models.ForeignKey(NavigatorModel, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=uploadedFilePath)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    fileName = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.fileName} uploaded on {self.uploaded_at}"
    
    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        # Call the parent class's delete method to delete the instance from the database
        super().delete(*args, **kwargs)
    
@receiver(pre_delete, sender=User)  # This line connects the function below to the pre_delete signal for the User model
def deleteUserFileUploadPath(sender, instance, **kwargs):
    userFileUploadPath = os.path.join('media', instance.username)
    if os.path.exists(userFileUploadPath):
        shutil.rmtree(userFileUploadPath)