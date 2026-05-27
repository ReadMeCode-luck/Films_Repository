from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView
from .models import Film


def index(request):
    films = Film.objects.all()
    context = {
        'films': films
    }
    return render(request, 'home.html', context)


class FilmList(ListAPIView):
    queryset = Film.objects.all()


def entrance(request):
    return redirect('login')

