from django.contrib import admin
from accounts.models import UserProfile
from import_export.admin import ImportExportModelAdmin


class UserProfileAdmin(ImportExportModelAdmin):
    list_display = (
        'user',
        'university',
        'location',)
    search_fields = [
        'user__username',
    ]

    # def get_signup_source(self, obj):
    #     return obj.get_signup_source_display()
    # get_signup_source.short_description = 'Signup Source'
    #
    # # pylint: disable=no-self-use
    # def get_registration_source(self, obj):
    #     return obj.get_registration_source_display()
    # get_registration_source.short_description = 'Registration Source'

admin.site.register(UserProfile, UserProfileAdmin)