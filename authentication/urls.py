
from django.contrib import admin
from django.urls import path

from authentication.views import *


urlpatterns = [
    path('signup', SignUpView.as_view()),
    path('getme', GetMeView.as_view()),
    path('signin', SignInView.as_view())
]
