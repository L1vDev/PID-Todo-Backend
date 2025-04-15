from rest_framework import serializers
from app_auth.models import User
from app_auth.utils import generate_token, send_reset_password_email
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    picture=serializers.ImageField(write_only=True,allow_null=True)
    picture_url=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=["id","username","password","email","picture_url","picture"]

    def get_picture_url(self,obj):
        if obj.picture:
            return obj.cloud_url
        return None
    
    def create(self, validated_data):
        request = self.context.get('request')
        user=User(**validated_data)
        user.set_password(validated_data["password"])
        return user

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user is associated with this email address")
        return value

    def save(self, **kwargs):
        request = self.context.get('request')
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token = generate_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # URL to reset the password
        reset_url = f"{request.scheme}://{request.get_host()}/reset-password/confirm/{uid}/{token}/"

        try:
            send_reset_password_email(user,reset_url)
        except Exception as e:
            print(str(e))

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New password and confirm password do not match"})
        return data

    def save(self, user, **kwargs):
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
