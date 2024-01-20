
from django.contrib import admin
from django.urls import path
from authentication.controllers.get_me_controller import GetMeController
from authentication.controllers.sign_in_controller import SignInController
from authentication.controllers.sign_up_controller import SignUpController


urlpatterns = [
    path('signup', SignUpController.as_view()),
    path('getme', GetMeController.as_view()),
    path('signin', SignInController.as_view())
]
