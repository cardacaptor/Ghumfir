from ghumfir.utils.exceptions import *
from rest_framework import serializers
import re
# if re.search("[0-9]", password): passwprd contains number 
# if re.search("[a-z]", password) or re.search("[A-Z]", password): passwprd contains a letter

class UserValidatorBasic():
    def validate_character_count8(value):
        if len(value) < 8:
            raise serializers.ValidationError("value must have atleast 8 characters")
        return value
               
    def validate_no_spaces(value):
        if " " in value:
            raise serializers.ValidationError("value cannot contain spaces")
        return value
    
    def validate_character_count3(value):
        if len(value) < 3:
            raise serializers.ValidationError("value must have atleast 3 characters")
        return value
    
    def type_string(value):
        if not isinstance(value, str):
            raise serializers.ValidationError("value must be in string format")
        return value.strip()
    
    def validate_1_number(value):
        if not re.search("[0-9]", value):
            raise serializers.ValidationError("value must contain atleast 1 number")
        return value
    
    def validate_1_letter(value):
        if not (re.search("[a-z]", value) or re.search("[A-Z]", value)):
            raise serializers.ValidationError("value must contain atleast 1 letter")
        return value
    
    signup_username_validator = [type_string, validate_character_count3]
    signup_password_validator = [type_string, validate_character_count8, validate_no_spaces, validate_1_letter, validate_1_number]
    signup_email_validator = [type_string]

    signin_username_validator = [type_string]
    signin_password_validator = [type_string]