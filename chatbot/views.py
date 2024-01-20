from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["Get",])
def hello_chatbot(request):
    return Response({"data": "Hello World"})