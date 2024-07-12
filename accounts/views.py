from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import UserModel
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
import smtplib
from django.http import HttpResponse

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
        print(email)
        print(request.data)

        if email is None:
            return Response({'message':'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = UserModel.objects.get(email=email)

        except UserModel.DoesNotExist:
            return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.userID))
        reset_link = f'{settings.FRONTEND_URL}/reset-password/{uid}/{token}'

        send_mail(
            'Password Reset Request',
            f'Click the following link to reset your password: {reset_link}',
            'yash.test.noreply@gmail.com',
            [email],
            fail_silently=False,
        )

        return Response({'message':'Password reset link sent to your email'}, status=status.HTTP_200_OK)


def test(request):
    sender_email = 'yash.test.noreply@gmail.com'
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Enable TLS
            # server.login(sender_email, sender_password)
            # text = message.as_string()
            # server.sendmail(sender_email, recipient_email, text)
            return HttpResponse('Email sent successfully')
    except Exception as e:
        return HttpResponse(str(e))



        






def register(request):
    return render(request, 'accounts/signup.html')

def home(request):
    return render(request, 'accounts/login.html')

def ForgotPassword(request):
    return render(request, 'accounts/forgot.html')