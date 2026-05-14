from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Film

def index(request):
    films = Film.objects.all()
    context = {
        'films': films
    }
    return render(request, '', context)

class FilmList(ListAPIView):
    queryset = Film.objects.all()

