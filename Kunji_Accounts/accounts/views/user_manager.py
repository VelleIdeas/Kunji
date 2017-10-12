import logging
import datetime

from django.contrib.auth.models import User
from django.utils.encoding import smart_text
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from accounts.views.base_user_manager import BaseUserManager
from accounts.models import UserProfile

_logger = logging.getLogger(__name__)


class UserManagerImpl(BaseUserManager):

    def __init__(self, request_dict={}):
        self._request_dict = request_dict

    def populate_user(self, email):
        '''
        This method used to populate user from request

        :param email: email of the user
        :returns user object which contains user info
        '''
        user = User.objects.get(email=email)
        return user

    def create_user(self):
        '''
        This will handle below things:
        * adding user
        * adding user to related groups

        :param company: company object
        :returns user object
        '''

        input_dict = self._request_dict
        input_dict['firstName'] = sanitize_name_db(
            input_dict.get('firstName', ''))
        input_dict['lastName'] = sanitize_name_db(
            input_dict.get('lastName', ''))
        _logger.info("create_user - Start")
        cleaned_dict = input_dict.copy()
        cleaned_dict.pop("password", None)
        _logger.debug("input_dict: %s" % smart_text(cleaned_dict))

        user = User(
            username=input_dict['username'],
            email=input_dict['email'],
            first_name=input_dict['firstName'],
            last_name=input_dict['lastName'],
            is_active=False
        )

        user_password = input_dict.get('password')
        temp_password_set = False
        if not user_password:
            from utils import util
            _logger.info("Setting temp password for user: %s" % user.email)
            user_password = util.generatePassword()
            temp_password_set = True

        user.set_password(user_password)
        user.save()

        # Add user under is_active node if isActive is True
        if (input_dict['isActive'] == 'true' or input_dict['isActive']
            or input_dict['isActive'] == 1):
            user.is_active = True
            user.save()

        return user

    @transaction.atomic
    def update_user(self):
        '''
        This will handle below things:
        * update user data
        * update user groups which contains add/remove group
        * update company if required
        * update user email if required

        :param company: company object
        :returns added groups to that user
        '''

        _logger.debug('update_user - Start')
        input_dict = self._request_dict
        input_dict['firstName'] = sanitize_name_db(
            input_dict.get('firstName', ''))
        input_dict['lastName'] = sanitize_name_db(
            input_dict.get('lastName', ''))
        email = input_dict.get('email')
        user = User.objects.get(email=email)
        user.first_name = input_dict['firstName'][:30]
        user.last_name = input_dict['lastName'][:30]
        if input_dict['isActive'] is False or input_dict[
            'isActive'] == '0' or input_dict['isActive'] == 'false':
            user.is_active = False
        else:
            user.is_active = True
        user.save()

        _logger.debug('Before if')

        _logger.debug('update_user - End')
        return user.id

    def is_new_user(self, email):
        '''
        This method used to check given user is already exists or not

        :param email: email of the user
        :returns True or False
        '''
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return True
        return False

    def update_user_email(self, old_email, new_email):
        '''
        This method used for update the user email

        :param old_email: current email of the user
        :param new_email: new email
        '''
        _logger.debug('update user email')
        _logger.debug('updating %s to %s' % (old_email, new_email))
        user = User.objects.get(email=old_email)
        user.username = new_email
        user.email = new_email
        user.save()
        return

    def remove_active_user_access(self, user, group_name):
        """
        This method used for remove user to given group
        :param group_name: name of the group
        """
        user.is_active = False
        user.save()

        user_profile = UserProfile.objects.get(user=user)
        user_profile.force_logout = datetime.datetime.utcnow()
        user_profile.save()
        return

    def enable_user_access(self, user):
        """
        This method used for enable the user access
        """
        user.is_active = True
        user.save()

        user_profile = UserProfile.objects.get(user=user)
        user_profile.force_logout = None
        user_profile.save()
        return

    def reset_user_password(self, email, new_password):
        '''
        This method used for reset the user password

        :param email: email of the user
        :param new_password: new password
        '''
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return


def sanitize_name_db(name):
    if 'Not Provided' in name:
        return ''
    return name
