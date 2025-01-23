from django.urls import path
from .. import views


urlpatterns = [
    # profile
    path('', views.ProfileApiView.as_view(), name='profile'),

]