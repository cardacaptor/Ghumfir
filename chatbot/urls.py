
from django.contrib import admin
from django.urls import path
from chatbot.controllers.get_chat_controller import ChatController
from chatbot.controllers.send_text_controller import SendTextController

urlpatterns = [
    path('', SendTextController.as_view(),),
    path('<int:page>', ChatController.as_view(),),
]
