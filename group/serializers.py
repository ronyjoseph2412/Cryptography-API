from django.contrib.auth.models import User
from rest_framework import serializers,validators
from .models import User_data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_data
        fields = ('image')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','email','first_name','last_name')
        extra_kwargs = {
            
            'password':{'write_only':True},
            'email':{
                'required':True,
                'allow_blank':False,
                'validators':[validators.UniqueValidator(queryset=User.objects.all(),message='A User with this email id already exists')]
            }
    }




    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            )
        return user