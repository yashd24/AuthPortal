from django.urls import path
from .views import ForgotPassword,home, register,RegisterView,LoginView,ForgotPasswordView,test

urlpatterns = [   
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('register-api/', RegisterView.as_view(), name='register-api'),
    path('login/', home, name='login'),
    path('login-api/', LoginView.as_view(), name='login-api'),
    path('forgot/', ForgotPassword, name='forgot'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password-api'),
    path('test/', test, name='test'),
    

               
]