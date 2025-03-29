from rest_framework import generics, status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import RegistrationSerializer


User = get_user_model ()

class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        # get serializer and use it on the request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # call create() method in the serializer and save the user
        user = serializer.save()
        # provide a token for the new user
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)




