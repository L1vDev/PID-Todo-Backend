from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from app_auth.models import User
from app_auth.serializers import UserSerializer, LoginSerializer, ChangePasswordSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer
from django.contrib.auth import authenticate
from app_auth.utils import generate_token,verify_token,send_verification_email
from django.utils.http import urlsafe_base64_decode
#import logging

#logger=logging.getLogger("app_auth_views")

class UserAccountView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() 
        user.save()
        token=generate_token(user)
        
        origin = request.META.get('HTTP_ORIGIN', 'Unknown')
        verification_url = f"{origin}/auth/verify-email/{token}"
        send_verification_email(user,verification_url,origin)
        
        return Response({
            'message': 'Usuario creado. Por favor verifica tu correo electrónico.',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    serializer_class=LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                if not user.is_email_verified:
                    token=generate_token(user)
                    origin = request.META.get('HTTP_ORIGIN', 'Unknown')

                    verification_url = f"{origin}/auth/verify-email/{token}"
                    send_verification_email(user,verification_url,origin)
                    return Response({"error": "Credenciales incorrectas, se ha enviado un correo de verificación"}, status=status.HTTP_404_NOT_FOUND)

                refresh = RefreshToken.for_user(user)
                return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                })
        return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            payload,token_is_valid=verify_token(token)
            if not token_is_valid:
                return Response({'details': 'Token expirado',"error":"invalid_token"},status=status.HTTP_401_UNAUTHORIZED)
        
            user = User.objects.filter(pk=payload["user_id"]).first()
            if user:
                user.is_email_verified = True
                user.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'details': 'Correo verificado con éxito!',
                    'user':user,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                    },status=status.HTTP_200_OK)
            return Response({'details': 'Token no valido',"error":"invalid_token"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"details":str(e),"error":"server_error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.validated_data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_406_NOT_ACCEPTABLE)

            # Set new password
            self.object.set_password(
                serializer.validated_data.get("new_password"))
            self.object.save()

            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"detail": "Se ha enviado un correo para restablecer la contraseña."}, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({"detail": "Ha ocurrido un error al intentar restablecer la contraseña."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None:
            payload, token_is_valid= verify_token(token)
            if token_is_valid:
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=user)
                    return Response({"detail": "Password has been reset with the new password."}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Invalid token or user ID"}, status=status.HTTP_400_BAD_REQUEST)


