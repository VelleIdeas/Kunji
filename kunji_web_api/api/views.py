import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from . import models

@csrf_exempt
def upload_paper(request):
    data = json.loads(request.body)
    print(data)
    id = data['id']
    imageData = data['imageData']
    data = {'foo': data['id']}
    #FileStore
    return HttpResponse(json.dumps(data), content_type='application/json')
    #return HttpResponse("OK")

  
def index(request):
    print('index')
    str = "Hello World"
    context = {'message' : str}
    return render(request, 'index.html', context)