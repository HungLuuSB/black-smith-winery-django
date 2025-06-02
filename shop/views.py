from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse('this shit works!')

def category(request, categorySlug: str):
    return render(request, 'shop/index.html')

