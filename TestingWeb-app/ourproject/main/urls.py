from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home.html', views.index),
    path('test.html', views.testing, name='test'),
    path('personal_account.html', views.user, name='user'),
    path('login.html', views.login, name='login'),
    path('test_form.html', views.test_form, name='test_form'),
]