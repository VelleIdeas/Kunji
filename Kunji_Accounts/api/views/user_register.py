import logging
import json
import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from accounts.models import UserProfile
from django.utils.encoding import force_text
from rest_framework.exceptions import APIException
from accounts.views.user_utils import create_or_edit_user

PASSWORD_REGEX = r'^.*(?=.{6,}).*$'
# A very rudimentary email regex. Just making sure you didn't type your
# name in the wrong box.
EMAIL_REGEX = r'^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*([a-zA-Z0-9-]+)?@[a-zA-Z0-9-]+(\.[a-zA-Z0-9]+)*$'

logger = logging.getLogger(__name__)


# Validation functions
def _required_field(field, data):
    val = data.get(field)
    if isinstance(val, str):
        val = val.strip()
    if not val:
        return 'Required'


def _validate_password(field, data):
    pw = data.get(field)
    return None


def _validate_email(field, data):
    email = data.get(field)
    if not email:
        return 'Email required.'
    if not re.match(EMAIL_REGEX, email):
        return 'Invalid email address.'
    users = User.objects.filter(email=email)
    if users:
        return 'This email is already registered with us.'
    return None


_signup_field_functions = [
    ("firstName", _required_field),
    ("lastName", _required_field),
    ("email", _validate_email),
    ("password", _validate_password),
    ("username", _required_field),
]


class SignupJSONParser(JSONParser):
    '''
    Parses and validates JSON payload for create_user API endpoint.
    '''

    media_type = 'application/json'

    def parse(self, stream, media_type, parser_context):
        try:
            data = super(SignupJSONParser, self).parse(
                stream, media_type, parser_context)
            logger.debug(data)
            errors = validate_signup_json(data)
            if errors:
                raise BadRequestError(errors)
            return data
        except Exception as ex:
            logger.exception(ex)
            raise ex


class BadRequestError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None):
        APIException.__init__(self, detail=detail, code=self.status_code)
        self.detail = force_text(detail)


def validate_signup_json(req_json):
    errors = {}

    def _validate(field, validation):
        err = validation(field, req_json)
        if err:
            errors[field] = err

    for field_name, val_func in _signup_field_functions:
        _validate(field_name, val_func)
    return ResponseDict(errors)


class ResponseDict(dict):
    def __str__(self):
        return json.dumps(self)


def sanitize_input_dict(request_dict, input_fields=None):
    """
    :param request_dict: The input dictionary.
    :param input_fields: List of keys in request_dict for which the values has to be sanitized.
    Removes html tags for input_fields fields in request dict.
    If input_fields is empty, the whole request_dict is sanitized.
    """
    data = request_dict.copy()
    if input_fields:
        for field in input_fields:
            try:
                val = data[field]
            except KeyError:
                data[field] = None
            else:
                if isinstance(val, unicode) or isinstance(val, str):
                    data[field] = val.strip()
    else:
        for key, val in data.iteritems():
            if val:
                if isinstance(val, unicode) or isinstance(val, str):
                    data[key] = val.strip()
    return data


def extract_signup_location_for_request(request_dict, request):
    logger.debug(
        "SignupLocation from  request dict is : %s" %
        request_dict.get(
            "signupLocation",
            "Not obtained"))
    if not request_dict.get("signupLocation"):
        logger.debug(
            "SignupLocation not set in request param, setting the location from the referer header")
        logger.debug(
            "SignupLocation from  request header is : %s" %
            request.META.get('HTTP_REFERER'))
        return request.META.get('HTTP_REFERER', '')
    logger.debug(
        "Signup location will be returned as : %s" %
        request_dict.get("signupLocation"))
    return request_dict.get("signupLocation")


@transaction.non_atomic_requests
@api_view(['POST'])
@permission_classes((AllowAny,))
@parser_classes((SignupJSONParser,))
def create_user(request):
    user_input_fields = [
        'firstName',
        'username',
        'lastName',
        'email',
    ]
    data = sanitize_input_dict(request.data, user_input_fields)
    data["signuplocation"] = extract_signup_location_for_request(data, request)
    data["isActive"] = 1
    logger.debug("data before setting User %s", data)
    try:
        new_uid = create_or_edit_user(
            data,
            create_only=True,
        )
    except Exception as ex:
        logger.exception(ex)
        raise ex

    # log user in
    user_password = data.get('password')
    if not user_password:
        user_profile = UserProfile.objects.get(user_id=new_uid)
        user_password = user_profile.password_token
    user = authenticate(username=data.get('username'), password=user_password)
    if user:
        logger.debug("user ID %s: is_active %s", user.id, user.is_active)

    if user is not None and user.is_active:
        login(request, user)

    return Response({
        "id": new_uid,
        "session_id": request.session.session_key
    })


@api_view(['POST'])
def create_profile(request):
    if request.method == 'POST':
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        data = request.data
        data = sanitize_input_dict(data)

        user_profile.university = data['university']
        user_profile.location = data['location']
        user_profile.save()

        return Response("Success")
