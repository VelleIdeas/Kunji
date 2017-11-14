import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from . import persistence

@csrf_exempt
def upload_paper(request):
    data = json.loads(request.body)
    #print(data)
    imageData = data['imageData']
    tags = data['tags']
    persistence.SavePaper(imageData, tags)
    data = {'result': 'success'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def get_papers(request):
    data = json.loads(request.body)
    print(data)
    tags = data['tags']
    photo_urls = persistence.GetPapers(tags)
    data = {'urls': photo_urls}
    return HttpResponse(json.dumps(data), content_type='application/json')
  
def index(request):
    print('index')
    str = "Hello World"
    context = {'message' : str}
    return render(request, 'index.html', context)