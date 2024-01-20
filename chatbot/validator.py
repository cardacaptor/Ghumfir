from ghumfir.utils.exceptions import *
from rest_framework import serializers

class MessageValidatorBasic():
    def type_string(value):
        if not isinstance(value, str):
            raise serializers.ValidationError("value must be in string format")
        return value.strip()
    
    chat_message_validator = [type_string]