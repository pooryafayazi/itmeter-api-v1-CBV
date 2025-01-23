from django.urls import path
from .. import views
from rest_framework_simplejwt.views import (TokenRefreshView,TokenVerifyView)


urlpatterns = [
    # login jwt
    path('create/', views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('verify/', TokenVerifyView.as_view(), name='jwt-verify'),   
    
]