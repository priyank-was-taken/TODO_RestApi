from django.db import models
from django_extensions.db.models import TimeStampedModel
# Create your models here.


class TodoList(TimeStampedModel):
    task = models.CharField(max_length=55)
    completed = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        verbose_name = 'TodoList'
        verbose_name_plural = 'TodoLists'

    def __str__(self):
        return self.task

