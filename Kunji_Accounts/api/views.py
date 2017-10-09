import logging
import json
import re
import ast

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework import status



@transaction.non_atomic_requests
@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):
    pass
