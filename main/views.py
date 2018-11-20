from decouple import config
from django.shortcuts import render, redirect
from area.rosreestrapi import Client

def home(request):
    return render(request, 'home.html')

