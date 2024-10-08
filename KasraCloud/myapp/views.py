# This Code is how the frontend connects to the backend
# Whenever the fetch command is called in the HTML templates, Django uses urls.py to connect to this file


from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse, HttpResponseNotFound
from .navigator import Navigator, File, Folder
import json
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.template import Template, Context
from django.contrib import messages
from .models import NavigatorModel, UserFiles
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
import os
from django.conf import settings 
import mimetypes
from wsgiref.util import FileWrapper



# Signup sends a request to the User model form in forms.py
# The form connects to the User model that Django offers, allowing for user authentication

def signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            NavigatorModel.objects.create(user=user)
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account was created for {username}")
            return redirect("start")
    context = {"form": form}
    return render(request, 'myapp/signUpScreen.html', context)

# This function collects the username and password of a user to then decide to send them to the home screen (where the app is) or to show error messages.

def start(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username OR Password is incorrect")
    return render(request, 'myapp/startScreen.html')

# this function simply logs out the user

def logoutUser(request):
    navigator = loadNavigator(request)
    navigator.resetScreen()
    saveNavigator(request, navigator)
    logout(request)
    messages.info(request, "Logged Out ")
    return redirect("start")

# loads a navigator model created in models.py by using functions within the model
# These functions start a navigator object from navigator.py which has the main functionality of the project

def loadNavigator(request):
    if request.user.is_authenticated:
        navigatorModel = NavigatorModel.objects.get(user=request.user)
        return navigatorModel.loadNavigatorHelper()



def saveNavigator(request, navigator):
    navigatorModel = NavigatorModel.objects.get(user=request.user)
    navigatorModel.saveNavigatorHelper(navigator)
    return

def home(request):
    if not request.user.is_authenticated:
        return redirect("start")
    
    navigator = loadNavigator(request)
    navigator.updateDisplay()
    
    fileIconTemplate = Template('{% load static %}{% static "myapp/Images/fileIcon.png" %}')
    folderIconTemplate = Template('{% load static %}{% static "myapp/Images/folderIcon.png" %}')
    
    fileIconUrl = fileIconTemplate.render(Context())
    folderIconUrl = folderIconTemplate.render(Context())
    
    navigator.display = navigator.display.replace('fileIconUrl', fileIconUrl)
    navigator.display = navigator.display.replace('folderIconUrl', folderIconUrl)
    
    
    
    if navigator.searched != False and navigator.currentFolder:
        currentFolder = f"<h1>(Search) {navigator.currentFolder.name}:</h1>"
    elif navigator.searched != False:    
        currentFolder = "<h1>Search:</h1>"
    elif navigator.currentFolder == None:
        currentFolder = "<h1>Main Screen:</h1>"
    else:
        currentFolder = f"<h1>{navigator.currentFolder.name}:</h1>"
    
    context = {"display": navigator.display, "currentFolder": currentFolder}
    saveNavigator(request, navigator) 
    return render(request, 'myapp/homeScreen.html', context)

def addFile(request):
    navigator = loadNavigator(request)
    name = request.POST.get("Name")
    uploadedFile = request.FILES["File"]
    fileType = request.POST.get("fileType")
    navigator.createFile(name, fileType)
    
    navigatorModel = NavigatorModel.objects.get(user=request.user)
    newFileName = f"{name}{fileType}"
    uploadedFile.name = newFileName
    UserFiles.objects.create(navigator=navigatorModel, file=uploadedFile, fileName=name)
    saveNavigator(request, navigator)
    return redirect("home")

def addFolder(request):
    navigator = loadNavigator(request)
    data = json.loads(request.body)
    name = data.get("Name")
    navigator.createFolder(name)
    saveNavigator(request, navigator) 
    return redirect("home")

def enterFolder(request):
    navigator = loadNavigator(request)
    data = json.loads(request.body)
    name = data.get("name")
    navigator.enterFolder(name)
    saveNavigator(request, navigator)
    return redirect("home")

def navigateUp(request):
    navigator = loadNavigator(request)
    navigator.navigateUp()
    saveNavigator(request, navigator)
    return redirect("home")

def search(request):
    navigator = loadNavigator(request)
    data = json.loads(request.body)
    name = data.get("name")
    navigator.search(name)
    saveNavigator(request, navigator)
    return redirect("home")

def getFilePath(request):
    data = json.loads(request.body)
    name = data.get("name")
    fileToFindPath = UserFiles.objects.get(navigator__user = request.user, fileName = name)
    return JsonResponse({"filePath": f"/media/{request.user.username}/{os.path.basename(fileToFindPath.file.name)}"})

def rename(request):
    navigator = loadNavigator(request)
    data = json.loads(request.body)
    name = data.get("name")
    newName = data.get("newNameForItem")
    itemType = data.get("type")
    if itemType == "File":
        fileType = navigator.everything[name].type
        fileOfficialNewName = newName + fileType
        fileToRename = UserFiles.objects.get(navigator__user=request.user, fileName=name)
        currentFilePath = fileToRename.file.path
        newFilePath = os.path.join(os.path.dirname(currentFilePath), fileOfficialNewName)
        os.rename(currentFilePath, newFilePath)
        fileToRename.fileName = newName
        fileToRename.file.name = os.path.join(os.path.dirname(fileToRename.file.name), fileOfficialNewName)
        fileToRename.save()
    navigator.rename(name, newName)
    saveNavigator(request, navigator)
    return redirect("home")

def checkEverything(request):
    navigator = loadNavigator(request)
    data = json.loads(request.body)
    name = data.get("name")
    if name in navigator.everything:
        return JsonResponse({'exists': True})
    else:
        return JsonResponse({'exists': False})
        
def delete(request):
    navigator = loadNavigator(request)
    data = json.loads(request.body)
    name = data.get("name")
    itemType = data.get("type")
    filesToDelete = navigator.delete(name)
    if itemType == "File":
        name = name.split(".")
        name = name[0]
        userFileBeingDeleted = UserFiles.objects.get(navigator__user=request.user, fileName=name)
        userFileBeingDeleted.delete()
    else:
        if isinstance(filesToDelete, list):
            for i in range(len(filesToDelete)):
                userFileBeingDeleted = UserFiles.objects.get(navigator__user=request.user, fileName=filesToDelete[i])
                userFileBeingDeleted.delete()
    saveNavigator(request, navigator)
    return redirect("home")

