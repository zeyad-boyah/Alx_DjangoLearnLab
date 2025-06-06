from rest_framework import generics, status, permissions
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from .serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer
from django.shortcuts import get_object_or_404
from notifications.views import create_follower_notification

# could use CustomUser.objects.all() from the models but i choose the less confusing way :sadge:
User = get_user_model()

class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        # get serializer and use it on the request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # call create() method in the serializer and save the user
        user = serializer.save()
        # get the token made in the serializer
        token= Token.objects.get(user=user)

        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        
        # USERNAME_FIELD = 'email' so this is why username=email
        user = authenticate(username=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return the currently authenticated user
        return self.request.user
    

class FollowUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('user_id')
        # get the user to follow by pk
        user_to_follow = get_object_or_404(self.get_queryset(), pk=pk)
        current_user = request.user

        # check if the user is trying to follow himself (would be sad though)
        if user_to_follow == current_user:
            return Response(
                {"detail":"sorry bro but you can't follow yourself try following me :)"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # check if already following
        if current_user.following.filter(pk=user_to_follow.pk).exists():
            return Response(
                {"detail": f"you are already following {user_to_follow.username})"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # add the user to following list
        current_user.following.add(user_to_follow)

        # Create a notification for the follow action
        create_follower_notification(actor=current_user, user=user_to_follow)

        return Response(
            {"detail": f"You are now following {user_to_follow.username}."},
            status=status.HTTP_200_OK,
        )
    
class UnFollowUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('user_id')
        user_to_unfollow= get_object_or_404(self.get_queryset(), pk=pk)
        current_user = request.user

        # check if user is actually following 
        if current_user.following.filter(pk=user_to_unfollow.pk).exists():
            current_user.following.remove(user_to_unfollow)
            return Response(
                {"detail": f"You have now unfollowed {user_to_unfollow.username}."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )