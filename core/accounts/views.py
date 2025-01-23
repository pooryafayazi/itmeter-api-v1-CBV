from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from .models import User
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()


'''    
class TestEmailSend(generics.GenericAPIView):
        
    def get(self, request, *args, **kwargs):
        self.email = 'sarbaz@sarbaz.com'
        user_obj = get_object_or_404(User, email = self.email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/hello.tpl', {'token': token}, 'admin@admin.com', to=[self.email])
        EmailThread(email_obj).start()
        return Response('Email sent')
    
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
 '''   
    


'''
class ResetPasswordConfirmApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, token, *args, **kwargs):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': _('Password has been reset successfully.')}, status=status.HTTP_200_OK)
 '''   
    
 
# from itmeneter
from django.shortcuts import redirect, render
from django.contrib import messages
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

from django.shortcuts import redirect
from django.urls import reverse

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email_user = request.POST.get('email')
            password = request.POST.get('password')

            # Attempt to authenticate using email
            user = authenticate(request, email=email_user, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect(reverse('blog:post_list'))
            else:
                messages.error(request, 'Invalid email or password.')

        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'accounts/login.html', context)
    else:
        return redirect(reverse('blog:post_list'))

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        return render(request, 'accounts/login.html' ) 
    return redirect(reverse('blog:post_list'))


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():                
                form.save()
                return redirect('accounts:login')  # Redirect to login page after signup
            else:
                return render(request, 'accounts/signup.html', {'form': form})  # Show form with errors
        else:
            form = CustomUserCreationForm()  # Use the custom form here
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        return render(request, 'blog/post_list.html' )