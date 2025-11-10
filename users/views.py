from rest_framework import generics
from django.contrib.auth import get_user_model
from users.serializers import RegisterSerializer

User = get_user_model()

class RegistrationView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
