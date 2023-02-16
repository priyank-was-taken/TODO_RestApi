from rest_framework import serializers
from . import models


class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TodoList
        fields = ["id", "task", "created", "modified", "completed"]

class ReadTodoListSerializer(serializers.ModelSerializer):
    completed = serializers.BooleanField(read_only=True)
    class Meta:
        model = models.TodoList
        fields = ["id", "task", "created", "modified", "completed"]