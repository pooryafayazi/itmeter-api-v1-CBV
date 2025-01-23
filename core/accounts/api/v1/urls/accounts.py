from django.urls import path
from .. import views


urlpatterns = [    
    # registration
    path('registration/', views.RegistrationApiView.as_view(),name='registration'),
    

    # change pasword
    path('change-password/',views.ChangePasswordApiView.as_view(), name='change-password'),    
   
    
    # path('test-email', views.TestEmailSend.as_view(), name='test_email'),
          
    # activation
    path('activation/confirm/<str:token>', views.ActivationApiView.as_view(),name='activation' ),
    
    
    # resend activation
    path('activation/resend/', views.ActivationResendApiView.as_view(), name='activation-resend'),  
    
    
         
    # reset password
    path('reset-password/',views.ResetPasswordApiView.as_view(), name='reset-password'),
    path('reset-password/confirm/<str:token>/', views.ResetPasswordConfirmApiView.as_view(), name='reset-password-confirm'),

]