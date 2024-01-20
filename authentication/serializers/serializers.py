
from rest_framework import serializers
from django.contrib.auth.models import User
from authentication.validators.user_validator import UserValidatorBasic

class SignUpSerializer(serializers.Serializer):
    
    validator = UserValidatorBasic()
    
    email = serializers.EmailField(validators = validator.signup_email_validator)
    username = serializers.CharField(validators = validator.signup_username_validator)
    password = serializers.CharField(validators = validator.signup_password_validator)
    
    def create(self, validated_data):  
        user = User.objects.create_user(**validated_data)
        user.save()
        return user
        
    def __str__(self):  
        return str({
            "username": self.username, 
            "email": self.email, 
            "password": self.password
            })
    

class SignInSerializer(serializers.Serializer):
    validator = UserValidatorBasic()

    username = serializers.CharField(validators = validator.signin_username_validator)
    password = serializers.CharField(validators = validator.signin_password_validator)
