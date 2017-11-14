import logging
from django.views.decorators.debug import sensitive_variables, \
    sensitive_post_parameters
from accounts.models import UserProfile, UserRegistrationSource
from accounts.views.user_manager import UserManagerImpl
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.db import transaction
from django.contrib.auth.models import User

_logger = logging.getLogger(__name__)


def get_user_profile(user):
    _logger.info('get_user_profile - Begin')
    try:
        profile = user.userprofile
    except ObjectDoesNotExist:
        _logger.info('Creating new user profile for user ' + user.email)
        # create profile - CUSTOMIZE THIS LINE TO YOUR MODEL:
        profile = UserProfile(user=user)
    _logger.debug('get_user_profile - End')

    return profile

def create_user_in_backend(email):
    """
    This function is to handle user in db if its not present there.
    """
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        #--------------------------------------------------------------#
        user_impl = UserManagerImpl()
        #--------------------------------------------------------------#
        user_impl.populate_user(email)
    except Exception as error:
        _logger.exception(str(error))


@sensitive_variables("password")
def create_or_edit_user(
        request_dict,
        create_only=False):
    _logger.info('create_or_edit_user -- start')
    _logger.info("Create or edit user request dict - %s", request_dict)
    request_dict['email'] = request_dict['email'].strip()
    registration_source = request_dict.get('registrationSource')
    if registration_source:
        if registration_source.lower() in (
                UserRegistrationSource.LINKEDIN.value,
                UserRegistrationSource.GOOGLE_PLUS.value,
                UserRegistrationSource.GITHUB.value):
            request_dict['socialAuthUser'] = True

    cleaned_dict = request_dict.copy()
    cleaned_dict.pop("password", None)
    _logger.debug("request dict: " + str(cleaned_dict))
    _email = str(request_dict['email'])
    _logger.debug('email:' + str(_email))

    _logger.debug('create_only = %s , registration_source - %s'
                  % (create_only, registration_source))

    user_impl = UserManagerImpl(request_dict)

    if user_impl.is_new_user(_email):
        _logger.debug('User %s does not exist.', _email)
        with transaction.atomic():
            user_impl._request_dict = request_dict
            user = user_impl.create_user()
    else:
        raise ValidationError('This email is already registered')
    return user.id