class File:
    def __init__(self, name, fileType):
        self.name = name
        self.type = fileType
    
 
    
class Folder:
    def __init__(self, name, contents = None):
        self.name = name
        if contents == None:
            self.contents = {}
        else:
            self.contents = contents

    def addFile(self, file):
        self.contents[file.name] = file
        return "File added"

    def addFolder(self, folder):
        self.contents[folder.name] = folder
        return "Folder added"

    def update_contents(self, new_contents):
        self.contents = new_contents

    def delete(self, name):
        if name in self.contents:
            object_type = type(self.contents[name]).__name__
            del self.contents[name]
            return f"{object_type} deleted"
        else:
            return "Name not found"  
    
    def request(self, object):
        answer = input(f"{type(object).__name__} of that name already exists, would you like to replace its content? (y/n)")
        answer = answer.strip().lower()
        return answer == "y"
    
    def rename(self, newName):
        self.name = newName
        return "Folder renamed"




                