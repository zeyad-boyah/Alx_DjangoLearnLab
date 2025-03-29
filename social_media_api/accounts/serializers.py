from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators= [password_validation.validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')


    """
    write_only=True: Ensures that passwords are not exposed in API responses aka INPUT ONLY.
    required=True: Makes both fields mandatory.
    validators=[password_validation.validate_password]: Applies Django's built-in password strength validation.
    """
    def validate(self, data):
        if data.get("password") != data.get("password2"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data
    
    # remove password2 as it is no longer needed
    def create(self, validated_data):
        validated_data.pop("password2")  # Remove the password confirmation field
        user = User.objects.create_user(**validated_data)  # Create user
        return user




class LoginSerializer(serializers.Serializer):
    # use email for authentication
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_picture']