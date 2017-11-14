from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def blank_page(request):
    return render(request, 'accounts/blank_page.html', locals())