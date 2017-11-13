from django.contrib import admin
from .models import Users, UserProfiles, Tags, Papers

admin.site.register(Users)
admin.site.register(UserProfiles)
admin.site.register(Tags)
admin.site.register(Papers)