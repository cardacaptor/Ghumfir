from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.permissions import * 
from rest_framework.generics import *
from django.contrib.auth.decorators import *
from drf_spectacular.utils import extend_schema

from ghumfir.utils.exceptions import MyValidationError

from ..serializers import *
from django.contrib.auth import *
from rest_framework.authtoken.models import Token
from ..models import *

#pagination methodologies
#cursor based
#offset based


# Create your views here.
class FeedView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Pagination

    def post(self, request, *args, **kwargs):
        pagination  =  Pagination(data = request.data)
        isValid = pagination.is_valid()
        if isValid:
            start = (pagination.data["page"] - 1) * pagination.data["size"]
            end = start + pagination.data["size"]
            posts = Post.objects.all().order_by('-id')
            data = PostSerializer(posts[start:end], many = True).data
            return Response({
                            "data":data, 
                            "status_code": 201,
                            "message": "Feed successfully loaded"
                            },
                            status= 200
                            )
        raise MyValidationError(pagination.errors)
