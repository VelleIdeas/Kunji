from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from enum import Enum


class BaseSourceEnum(Enum):

    @classmethod
    def choices(cls):
        choice_list = []
        for name, member in cls.__members__.items():
            member_tuple = (name, member.value)
            choice_list.append(member_tuple)
        return tuple(choice_list)

    @classmethod
    def get_name_from_value(cls, enum_value):
        for name, member in cls.__members__.items():
            if member.value == enum_value:
                return member.name

        raise ValueError("Non-standard signup/registration source '{}' given".format(enum_value))


class UserRegistrationSource(BaseSourceEnum):
    GOOGLE_PLUS = 'google-plus'
    FACEBOOK = 'facebook'
    SELF_SERVICE = 'self_service'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    university = models.CharField(max_length=100, blank=True)
    registration_source = models.CharField(
        max_length=20,
        choices=UserRegistrationSource.choices(),
        null=True,
        blank=True)
    password_token = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        app_label = 'accounts'
        db_table = 'user_profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
