from django.shortcuts import render

# Create your views here.
def home(request):
    return HttpResponse("Hello, your project is working!")