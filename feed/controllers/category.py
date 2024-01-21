from rest_framework.response import Response
from rest_framework.permissions import * 
from rest_framework.generics import *
from feed.model_serializers.category_serializer import CategorySerializer
from feed.models.category import Category
from ..serializers import *
from django.contrib.auth import *
from ..models import *


class CategoryController(GenericAPIView):
    permission_classes = []
    
    def get(self, request, *args, **kwargs):
        return Response({
                        "data": CategorySerializer(Category.objects.all(), many = True).data, 
                        "status_code": 200,
                        "message": "Categories successfully loaded",
                        },
                        status= 200
                        )