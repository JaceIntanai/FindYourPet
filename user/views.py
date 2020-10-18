from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import time

# Create your views here.
def about(request) :
    return render(request, "user/about.html")

def index(request) :
    return render(request, "user/homePage.html")