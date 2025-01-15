from django.urls import path
from .views import *

from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('home/', index, name='home'),

    path('', registration, name='reg'),
    
    path('login/', user_login, name='login'),
    path('activate/<str:uidb64>/<str:token>/', activision_check, name='activate'),
    path('logout/', user_logout, name="logout"),
    path('password_change',password_change,name='pass_change'),
    path('dashboard/', dashboard, name='dash'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('password_reset/', password_reset, name='pass_res'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
   

]
