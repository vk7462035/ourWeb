from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages



def index(request):
    return render(request, 'main/home.html')

def testing(request):
    return render(request, 'main/test.html')

def user(request):
    return render(request, 'main/personal_account.html')

def login(request):
    return render(request, 'main/login.html')

def test_form(request):
    return render(request, 'main/test_form.html')


