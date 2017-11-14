# contains code to interact with Models

from . import models, imageStore

def SavePaper(data, tags_text_array):
    #save the photo data to the store
    url = imageStore.StoreImageOnDisk(data)
    #print(url)
    
    #get the tags if they exist of create them.
    tag_list = []
    for tag_text in tags_text_array:
        tag,created = models.Tags.objects.get_or_create(text=tag_text)
        tag_list.append(tag)
    
    #Get the current logged-in user.
    #Using temp user 1 for now.
    user = models.Users.objects.get(pk=1)
    
    #Save paper object with url and tag list.
    paper = models.Papers.objects.create(photo_url=url, created_by_user=user)
    paper.tags.add(*tag_list)
    
    #Send the url back
    return url
    
def GetPapers(tags_text_array):
    tag_list = []
    for tag_text in tags_text_array:
        tag_list.append(tag_text)
    
    # Get all papers that have at least 1 of the tags.
    papers = models.Papers.objects.filter(tags__text__in=tag_list)
    
    photo_urls =[]
    
    for paper in papers:
        photo_urls.append(paper.photo_url)
        
    return photo_urls