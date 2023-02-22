from django.shortcuts import render
# from rest_framework.decorators import api_view
from rest_framework import views, status, generics, exceptions, decorators, response
from rest_framework_simplejwt.views import TokenViewBase, TokenObtainPairView
# from rest_framework.response import Response
from . import serializers
from . import models
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from datetime import datetime, timezone
import pyotp
from django.http import request, HttpResponse
import random
import base64
from rest_framework import viewsets
from django.core.mail import send_mail

def generate_otp(user):
    secret = base64.b32encode(user.encode())
    OTP = pyotp.TOTP(secret, interval=1000)
    return {'secret': secret, 'OTP': OTP.now()}

# Create your views here.
@decorators.api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>/',
    }
    return response.Response(api_urls)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#LIST
#fuction based veiw
@decorators.api_view(['GET'])
def apiList(request):
    task = models.TodoList.objects.all()
    serializer = serializers.TodoListSerializer(task, many=True)
    return response.Response(serializer.data)

# class based view
class ApiListView(views.APIView):

    def get(self, request):
        task = models.TodoList.objects.all().filter()
        serializer = serializers.TodoListSerializer(task, many=True)
        return response.Response(serializer.data)

# class based generic view
class ApiListGenericView(generics.ListAPIView):

    serializer_class = serializers.TodoListSerializer
    queryset = models.TodoList.objects.all()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#RETRIEVE
# function based view
@decorators.api_view(['GET'])
def apiDetail(request, pk):
    task = models.TodoList.objects.get(id=pk)
    serializer = serializers.TodoListSerializer(task)
    return response.Response(serializer.data)

# class based view
class APiRetrieveView(views.APIView):
    def get(self, request, pk):
        print(pk)
        try:
            task = models.TodoList.objects.get(id=pk)
            serializer = serializers.TodoListSerializer(task)
            return response.Response(serializer.data)
        except models.TodoList.DoesNotExist:
            return response.Response({'error': 'Task not found.'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)    

# class based generic view
class ApiRetrieveGenericView(generics.RetrieveAPIView):
    serializer_class = serializers.TodoListSerializer
    queryset = models.TodoList.objects.all()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# CREATE
# function based view
@decorators.api_view(['POST'])
def apiCreate(request):
    serializer = serializers.TodoListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return response.Response(serializer.data)

# class based view
class TaskCreateView(views.APIView):
    def post(self, request, format=None):
        serializer = serializers.TodoListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'error': 'Task not found.'},status=status.HTTP_400_BAD_REQUEST)

# generic class based view
class TaskCreateGenericView(generics.CreateAPIView):
    serializer_class = serializers.TodoListSerializer
    queryset = models.TodoList.objects.all()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#UPDATE
# function based view
@decorators.api_view(['POST'])
def apiUpdate(request, pk):
    task = models.TodoList.objects.get(id=pk)
    serializer = serializers.TodoListSerializer(instance=task,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return response.Response(serializer.data)

# class based view
class APiUpdateView(views.APIView):
    def put(self, request, pk):
        try:
            task = models.TodoList.objects.get(id=pk)
            serializer = serializers.TodoListSerializer(instance=task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data)
        except models.TodoList.DoesNotExist:
            return response.Response({'error': 'Task not found.'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)    

# class based generic view
# class ApiUpdateGenericView(generics.RetrieveUpdateAPIView):
#     serializer_class = serializers.TodoListSerializer
#     queryset = models.TodoList.objects.all()

class ApiUpdateGenericView(generics.RetrieveUpdateAPIView):
    queryset = models.TodoList.objects.all()
    serializer_class = serializers.TodoListSerializer

    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#DELETE
# function based view
@decorators.api_view(['DELETE'])
def apiDelete(request, pk):
    task = models.TodoList.objects.get(id=pk)
    task.delete()
    return response.Response("deleted")

# class based view
class ApiDeleteView(views.APIView):
    def get(self, request, pk):
        try:
            task = models.TodoList.objects.get(id=pk)
            task.delete()
            return response.Response("deleted")
        except models.TodoList.DoesNotExist:
            return response.Response({'error': 'Task not found.'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)    

# class based genric view
class ApiDeleteGenericView(generics.RetrieveDestroyAPIView):
    serializer_class = serializers.TodoListSerializer
    queryset = models.TodoList.objects.all()

class ApiRegisterView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    permission_classes = (AllowAny,)

class UserVerifyView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserVerifySerializer

    def post(self, request):
        key = request.data.get('secret_key')
        secret = base64.b32decode(key)
        email = secret.decode()
        print(email)
        try:
            user = models.User.objects.get(email=email)
            print(user)
        except models.User.DoesNotExist:
            return response.Response('user is not exists')

        otp = generate_otp(email)

        if request.data.get('otp') == otp.get('OTP'):
            print(user.is_verified)
            user.is_verified = True
            print(user.is_verified)
            user.save()
            # refresh = TokenObtainPairSerializer.get_token(user)

            data = {
                # 'refresh': str(refresh),
                # 'access': str(refresh.access_token),
                'user': serializers.UserSerializer(user).data,
            }
            return response.Response(data)
        else:
            return response.Response('Wrong OTP')
# class RegisterApi(views.APIView):

#     def post(self, request):
#             data = request.data
#             serializer = serializers.RegisterSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 (serializer.data['email'])
#                 return Response({
#                     'status': 200,
#                     'message': 'registration successfully check mail',
#                     'data': serializer.data,
#                 })

#             return Response({
#                 'status': 400,
#                 'message': 'something went wrong',
#                 'data': serializer.errors,
#             })
            
# class RegisterApi(APIView):

#     def post(self, request):
#             data = request.data
#             serializer = UserSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 send_otp_via_mail(serializer.data['email'])
#                 return Response({
#                     'status': 200,
#                     'message': 'registration successfully check mail',
#                     'data': serializer.data,
#                 })

#             return Response({
#                 'status': 400,
#                 'message': 'something went wrong',
#                 'data': serializer.errors,
#             })


# class VerifyOTP(APIView):
#     def post(self, request):
#         data = request.data
#         serializer = VerifyAccountSerializer(data = data)

#         if serializer.is_valid():
#             email = serializer.data['email']
#             otp = serializer.data['otp']

#             user = User.objects.filter(email = email)
#             if not user.exists():
#                 return Response({
#                     'status': 400,
#                     'message': 'something went wrong',
#                     'data': 'invalid email',
#                 })

#             if user[0].otp != otp:
#                 return Response({
#                     'status': 400,
#                     'message': 'something went wrong',
#                     'data': 'invalid otp',
#                 })
#             user = user.first()
#             user.is_verified = True
#             user.save()

#             return Response({
#                 'status': 200,
#                 'message': 'account verified',
#                 'data': {},
#             })

#         return Response({
#             'status': 400,
#             'message': 'something went wrong',
#             'data': serializer.errors,
#         })

# class OtpView(viewsets.ModelViewSet):
#     queryset = models.User.objects.all()
#     serializer_class = serializers.UserVerificationSerializer
#     model = models.User
#     permission_classes = (AllowAny,)

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = serializers.LoginSerializer
    
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         user = serializer.validated_data['user']
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
#         refresh_token = str(refresh)

#         # Set access token as HttpOnly cookie
#         response.set_cookie(key='access_token', value=access_token, httponly=True, secure=settings.SESSION_COOKIE_SECURE, expires=datetime.now(tz=timezone.utc) + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])

#         # Set refresh token as regular cookie
#         response.set_cookie(key='refresh_token', value=refresh_token, secure=settings.SESSION_COOKIE_SECURE, expires=datetime.now(tz=timezone.utc) + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])

#         return response  

# class LoginApiView(TokenObtainPairView):
#     serializer_class = serializers.LoginSerializer

class LoginApiView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Set the JWT token as a cookie on the response
            access_token_cookie_key = settings.SIMPLE_JWT.get('AUTH_COOKIE', 'access_token')
            response.set_cookie(
                key=access_token_cookie_key, 
                value=response.data['access'],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            
        return response