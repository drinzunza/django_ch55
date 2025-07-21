from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse

# Create your views here.

class UserLogin(LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        # where to go after login
        return reverse('home')