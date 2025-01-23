from django.urls import path
from .. import views


urlpatterns = [     
    # login token
    path('login/', views.CustomObtainAuthToken.as_view(), name='token-login'),
    path('logout/', views.CustomDiscardAuthToken.as_view(), name='token-logout'),    
    
]