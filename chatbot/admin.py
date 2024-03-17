from django.contrib import admin

from chatbot.models import ChatMessage, MessagePost

# Register your models here.

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("isBotMessage", "message", "user", "created")

class MessagePostAdmin(admin.ModelAdmin):
    list_display = ("message", "post")

admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(MessagePost, MessagePostAdmin)