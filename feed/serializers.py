from rest_framework import serializers

class UserActionSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
