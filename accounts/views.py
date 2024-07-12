from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import UserSerializer,ForgotPasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import UserModel
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import permission_classes,api_view


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User Registered Successfully'}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        
        user = UserModel.objects.filter(Q(username=username) | Q(email=username)).first()

        if user is None:
            return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({'message':'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({'message':'Login Successful',
                         'access' : str(refresh.access_token),
                         'refresh': str(refresh)
                         
                         }, status=status.HTTP_200_OK)
    
        

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        email = request.data['email']
        user = UserModel.objects.get(email=email)

        if email is None:
            return Response({'message':'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = UserModel.objects.get(email=email)

        except UserModel.DoesNotExist:
            return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.userID))
        reset_link = f'{settings.FRONTEND_URL}/auth/change-password/{uid}/{token}'

        serializer = ForgotPasswordSerializer(data={'email':email, 'token':token})

        if serializer.is_valid():
            try:
                serializer.save()
                send_mail(
                    'Password Reset Request',
                    f'Click the following link to reset your password: {reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return Response({'message':'Password reset link sent to your email'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password']
        uid_bytes = urlsafe_base64_decode(request.data['uid'])             #return in bytes
        userID = uid_bytes.decode('utf-8')                                 #convert bytes to string

        user = UserModel.objects.get(userID=userID)


        if old_password is None or new_password is None or confirm_password is None:
            return Response({'message':'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.check_password(old_password) == False:
            return Response({'message':'Old Password in Incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.check_password(old_password) and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            return Response({'message':'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response({'message':'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        

  




def register(request):
    return render(request, 'accounts/signup.html')

def login(request):
    return render(request, 'accounts/login.html')

def ForgotPassword(request):
    return render(request, 'accounts/forgot_password.html')

def change_password(request,uid,token):
    return render(request, 'accounts/change_password.html', {'uid':uid, 'token':token})

def dashboard(request):
    return render(request, 'accounts/dashboard.html')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_dashboard(request):
    user = request.user
    user_data = {
        "username": user.username,
        "email": user.email,
        "date_joined": user.date_joined
    }
    return Response(user_data)


@api_view(['POST'])  
@permission_classes([IsAuthenticated])  
def logout_func(request):
    return Response({'message':'Logged out successfully'}, status=status.HTTP_200_OK)
