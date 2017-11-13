from django.db import models

class Users(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    
    def __str__(self):              # __unicode__ on Python 2
        return self.user_name

class UserProfiles(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    
    def __str__(self):              # __unicode__ on Python 2
        return self.display_name
    
class Tags(models.Model):
    text = models.CharField(max_length=100)
    
    def __str__(self):              # __unicode__ on Python 2
        return self.text
    
class Papers(models.Model):
    photo_url = models.URLField(max_length=500)
    created_by_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    
    def __str__(self):              # __unicode__ on Python 2
        return self.photo_url
        return self.photo_url