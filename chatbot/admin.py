from django.contrib import admin

from chatbot.models import ChatMessage, MessagePost

# Register your models here.

admin.site.register(ChatMessage)
admin.site.register(MessagePost)