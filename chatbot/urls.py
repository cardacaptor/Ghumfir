
from django.contrib import admin
from django.urls import path

from chatbot.views import hello_chatbot

urlpatterns = [
    path('', hello_chatbot),
]
