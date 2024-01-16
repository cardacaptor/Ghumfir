from rest_framework import serializers

class Pagination(serializers.Serializer):
    page = serializers.IntegerField(default = 1)

class PaginationWithSearch(serializers.Serializer):
    page = serializers.IntegerField(default = 1)
    search = serializers.CharField()
