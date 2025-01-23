from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (RegistrationSerializer,CustomAuthTokenSerializer,
                          CustomTokenObtainPairSerializer,ChangePasswordSerializer,
                          ProfileSerializer,ActivationResendSerializer,
                          ResetPasswordSerializer,ResetPasswordConfirmSerializer)
from rest_framework.authtoken.views import ObtainAuthToken,APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
# from django.core.mail import send_mail
from mail_templated import send_mail
from mail_templated import EmailMessage
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.utils.translation import gettext_lazy as _

from datetime import datetime
import datetime
import pytz
from .utils import EmailThread
from ...models import Profile
from ...models import UsedResetToken
from django.conf import settings
# from ...models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data = {
                'email': email                
            }
            user_obj = get_object_or_404(User, email = email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'admin@admin.com', to=[email])
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
    
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


  

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
        


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)




class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    



class ChangePasswordApiView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'details':'password changed successfully' }, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
 
    
    
    
class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj    




class ActivationApiView(APIView):
    
    def get(self, request, token, *args, **kwargs):
        # decode > id user
        try:  
            token = jwt.decode(token, settings.SECRET_KEY , algorithms=["HS256"])
            user_id = token.get('user_id')
        except ExpiredSignatureError:
            return Response({'details':'token has been expired'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({'details':'token is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        # object user
        user_obj = User.objects.get(pk = user_id)
        
        if user_obj.is_verified:
            return Response({'details':'Your account has already verified.'})      
        user_obj.is_verified = True
        user_obj.save()
        return Response({'details':'Your account has been verified and activated successfully.'})
    
    



class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer
    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user']
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'admin@admin.com', to=[user_obj.email])
        EmailThread(email_obj).start()
        return Response({'details':'User activation resend successfully'}, status=status.HTTP_200_OK)
         
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    

    
    
class ResetPasswordApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user']
        token = self.generate_reset_token(user_obj)
        email_obj = EmailMessage('email/reset_password.tpl', {'token': token}, 'admin@admin.com', to=[user_obj.email])
        EmailThread(email_obj).start()
        return Response({'details': 'Password reset email sent successfully'}, status=status.HTTP_200_OK)
    def generate_reset_token(self, user):
        local_tz = pytz.timezone('Asia/Tehran')        
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.now(local_tz) + datetime.timedelta(hours=12) 
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
    




class ResetPasswordConfirmApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, token, *args, **kwargs):
        try:
            if UsedResetToken.objects.filter(token=token).exists():
                return Response({'detail': _('This token has already been used.')}, status=status.HTTP_400_BAD_REQUEST)

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return Response({'detail': _('Invalid or expired token.')}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        UsedResetToken.objects.create(token=token , user_id=user_id, email=user.email)

        return Response({'detail': _('Password has been reset successfully.')}, status=status.HTTP_200_OK)
    
    

        
    
