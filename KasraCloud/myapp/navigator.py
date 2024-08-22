from .fileAndFolder import File, Folder


class Navigator:
    def __init__(self):
        self.mainContent = {}
        self.current = self.mainContent
        self.path = []
        self.display = ""
        self.currentFolder = None
        self.everything = {}
        self.searched = False  # Will store the search input if searched
        self.allWithin = []
        self.placeHolder = {}

    def createFolder(self, name):
        new = Folder(name)
        self.current[name] = new
        self.everything[name] = new
        return "Folder created"

    def createFile(self, name, fileType):
        new = File(name, fileType)
        self.current[name] = new
        self.everything[name] = new
        self.updateDisplay()
        return "File created"

    def enterFolder(self, name):
        if name in self.current and isinstance(self.current[name], Folder):
            self.currentFolder = self.current[name]
            self.current = self.currentFolder.contents  # Update to the folder's contents
            if not self.searched:
                self.path.append(name)  # Append the folder to the path
            self.updateDisplay()
            return "Folder entered"
        return "Name not found"

    def navigateUp(self):
        self.searched = False
        if self.path:
            self.path.pop()
            pathPlaceholder = self.path[:]
            self.resetScreen()
            for folder in pathPlaceholder:
                self.enterFolder(folder)
            return "Navigated up"
        else:
            self.resetScreen()
            return "Already at the beginning"

    def updateDisplay(self):
        if not self.current:
            self.display = "<h2>Empty</h2>"
            return "Display updated"
        namesList = list(self.current.keys())
        self.display = ""
        for i in range(len(namesList)):
            object_type = type(self.current[namesList[i]]).__name__
            if object_type == "File":
                fileName = namesList[i] + self.current[namesList[i]].type
                imgSrc = "fileIconUrl"  # Placeholder for file icon URL
                self.display += f'<h2 class="{object_type}" data-name="{namesList[i]}" data-type="{object_type}"><img src="{imgSrc}" alt="File Icon" class="icon">{fileName}</h2>'
            else:
                imgSrc = "folderIconUrl"  # Placeholder for folder icon URL
                self.display += f'<h2 class="{object_type}" data-name="{namesList[i]}" data-type="{object_type}"><img src="{imgSrc}" alt="Folder Icon" class="icon">{namesList[i]}</h2>'
        return "Display updated"
    
    def allFilesWithinFolder(self, folderContents):
        files = []
        for item in folderContents:
            if isinstance(folderContents[item], File):
                files += [f"{folderContents[item].name}"]
            else:
                files += self.allFilesWithinFolder(item.contents)
        return files
            
    
    def delete(self, name):
        filesToDelete = None
        if self.searched != False:
            print(f"Deleting from searched: {self.searched}")
            folderWithContent = self.findItem(name)
            if isinstance(self.current[name], Folder):
                filesToDelete = self.allFilesWithinFolder(folderWithContent[name].contents)
            print(f"Files to delete: {filesToDelete}")
            del folderWithContent[name]
            return filesToDelete
        if name in self.current:
            print(f"Deleting from current: {self.current}")
            if isinstance(self.current[name], Folder):
                filesToDelete = self.allFilesWithinFolder(self.current[name].contents)
            print(f"Files to delete: {filesToDelete}")
            del self.current[name]
            return filesToDelete
        else:
            return "Name not found"

    def search(self, input):
        self.resetScreen()
        self.current = {}
        inputLength = len(input)
        for name in self.everything:
            if input.lower() == name.lower().strip()[:inputLength]:
                self.current[name] = self.everything[name]
        self.searched = input 
        return "Search result given"

    def resetScreen(self):
        self.current = self.mainContent
        self.currentFolder = None
        self.path = []
        self.searched = False
        self.updateDisplay()
        return "Screen reset"

    def openItem(self, name):
        if type(self.current[name]) == Folder:
            self.enterFolder(name)
            return "Item opened"
        return "Not a folder"

    def rename(self, name, newName):
        if newName not in self.everything:
            if self.searched != False:
                folderWithContent = self.findItem(name)
                folderWithContent[newName] = folderWithContent.pop(name)
                return "Item deleted"
            self.current[newName] = self.current.pop(name)
            return "Item renamed"
        else:
            return "Name already exists"
    

    def findItemHelper(self, name, searching):
        # Check if the name exists directly in the current searching folder
        if name in searching:
            return searching  # Return the contents of the folder where the item was found

        # Iterate through the items in the current folder
        for item in searching:
            if isinstance(searching[item], Folder):
                found = self.findItemHelper(name, searching[item].contents)
                if found != "Not Found":
                    return found  # Return the contents of the folder where the item was found

        return "Not Found"

    def findItem(self, name):
        searching = self.mainContent
        if name in searching:
            return searching  # If the item is found in the root folder, return the root folder's contents
        else:
            return self.findItemHelper(name, searching)  # Search recursively in subfolders
    
    def serialize(self):
        return {
            'mainContent': self.serialize_folder(self.mainContent),
            'path': self.path,
            'searched': self.searched,
            "currentFolder": self.currentFolder.name if self.currentFolder else None
        }

    def serialize_folder(self, folder):
        serialized_folder = {}
        for name, item in folder.items():
            serialized_folder[name] = self.serialize_item(item)
        return serialized_folder

    def serialize_item(self, item):
        if isinstance(item, File):
            return {
                'type': 'File',
                'name': item.name,
                'fileType': item.type,
            }
        elif isinstance(item, Folder):
            return {
                'type': 'Folder',
                'name': item.name,
                'contents': self.serialize_folder(item.contents)
            }
        return None

    def deserialize(self, data):

        # Resetting Navigator to its initial state before deserialization
        self.resetScreen()

        # Deserializing folders and files
        def add_items_from_data(current_folder, contents):
            for name, item_data in contents.items():
                if item_data['type'] == 'File':
                    self.createFile(name, item_data['fileType'])
                elif item_data['type'] == 'Folder':
                    self.createFolder(name)
                    # Enter the folder and add its contents
                    self.enterFolder(name)
                    add_items_from_data(self.current, item_data['contents'])
                    self.navigateUp()  # Go back to the parent folder after adding items

        add_items_from_data(self.mainContent, data['mainContent'])



        # Restoring search state, if applicable
        if data.get('searched') != False:
            # Handle the case where search is active
            self.search(data['searched'])
            self.currentFolder = self.everything.get(data["currentFolder"], None)
            if self.currentFolder:
                self.current = self.currentFolder.contents
        else:
            # If not searched, follow the path
            for folder in data.get('path'):
                self.enterFolder(folder)
        self.updateDisplay()
