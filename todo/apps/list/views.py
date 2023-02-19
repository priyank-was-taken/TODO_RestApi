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

class LoginApiView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer

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