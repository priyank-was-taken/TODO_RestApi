from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ["task", "completed"]


