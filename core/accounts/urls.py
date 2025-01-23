from django.urls import path,include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    
    # for api-v1
    path('api/v1/', include('accounts.api.v1.urls')),
    
    # for api-v2
    # path('api/v2/', include('djoser.urls')),
    # path('api/v2/', include('djoser.urls.jwt')),
     
    # from itemeter
    path('login/', views.login_view ,name='login'),
    path('logout', views.logout_view ,name='logout'),
    path('signup', views.signup_view ,name='signup'),  
]
