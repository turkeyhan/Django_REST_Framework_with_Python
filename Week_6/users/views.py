from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import RegisterSerializer

# CreateAPIView(generics) 사용 구현
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer