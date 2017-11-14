import uuid
import os

def StoreImageOnDisk(content):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    basePath = os.path.join(current_dir, "content")
    
    #Create a random file name
    fileName = str(uuid.uuid4())
    filePath = os.path.join(basePath, fileName)
    
    #Write the content to the file
    file = open(filePath, "w")
    file.write(content)
    file.close()
    
    #return the url of the file back
    return filePath
    
def StoreImageOnCloud(content):
    return "cloud url"
    
def ReadFromUrl(url):
    return "base64 encoded string"