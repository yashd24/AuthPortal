from django.urls import path
from .views import ForgotPassword,login, register,change_password,logout_func,dashboard,api_dashboard,RegisterView,LoginView,ForgotPasswordView,ChangePasswordView

urlpatterns = [   
    path('', login, name='login'),
    path('register/', register, name='register'),
    path('register-api/', RegisterView.as_view(), name='register-api'),
    path('login/', login, name='login'),
    path('login-api/', LoginView.as_view(), name='login-api'),
    path('forgot/', ForgotPassword, name='forgot'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password-api'),
    path('change-password/<str:uid>/<str:token>/', change_password, name='change-password'),
    path('change-password-api/', ChangePasswordView.as_view(), name='change-password-api'),
    path('dashboard/', dashboard, name='dashboard'),
    path('api/dashboard/', api_dashboard, name='api-dashboard'),
    path('logout/', logout_func, name='logout'),
]