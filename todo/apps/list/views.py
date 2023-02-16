from django.shortcuts import render
# from rest_framework.decorators import api_view
from rest_framework import views, status, generics, exceptions, decorators, response
# from rest_framework.response import Response
from . import serializers
from . import models


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
    serializer_class = serializers.ReadTodoListSerializer
#     # lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.completed:
            # If `completed` field is True, only allow updates to non-`completed` fields
            if 'completed' in request.data and request.data['completed']:
                serializer = serializers.TodoListSerializer(instance, data=request.data, partial=True)
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return response.Response(serializer.data)
    # def update(self, request, *args, **kwargs):
    #     print("11111")
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}

    #     return response.Response(serializer.data)

    # def perform_update(self, serializer):
    #     serializer.save()

    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)
    
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