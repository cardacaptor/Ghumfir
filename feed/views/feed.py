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
import ghumfir

from ghumfir.utils.exceptions import MyValidationError
import recommendation

from ..serializers import *
from django.contrib.auth import *
from rest_framework.authtoken.models import Token
from ..models import *

from drf_yasg.utils import swagger_auto_schema
#pagination methodologies
#cursor based
#offset based


# Create your views here.
class FeedView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Pagination
    
    def put(self, request, *args, **kwargs):
        pagination  = Pagination(data = request.data)
        isValid = pagination.is_valid()
        if isValid:
            start = (pagination.data["page"] - 1) * pagination.data["size"]
            end = start + pagination.data["size"]
            corpus_liked = ghumfir.wsgi.recommendation.get_corpus_by_index(pagination.data["liked"])
            posts =  ghumfir.wsgi.recommendation.sort_rest(pagination.data["liked"])
            return Response({
                            "corpus_liked":corpus_liked,
                            "data": posts[start+1:end+1], 
                            "status_code": 201,
                            "message": "Feed successfully loaded"
                            },
                            status= 200
                            )
        raise MyValidationError(pagination.errors)
    
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
