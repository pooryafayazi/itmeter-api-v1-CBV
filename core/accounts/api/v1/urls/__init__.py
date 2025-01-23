from django.urls import path,include

urlpatterns = [
    path('', include('accounts.api.v1.urls.accounts')),
    path('profile/', include('accounts.api.v1.urls.profile')),
    path('token/', include('accounts.api.v1.urls.token')),
    path('jwt/', include('accounts.api.v1.urls.jwt')),

]