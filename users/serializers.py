from rest_framework import serializers
from django.contrib.auth import get_user_model
# from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serilaizers.CharField(write_only=True, min_length=6)
    confirm_password = serilaizers.CharField(write_only=True, min_length=6

    class Meta:
        model=User
        fields=['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            return serializers.ValidationError({'confirm_password': "password not match"})
        # validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
            password=validated_data['password']
        )
        return user
