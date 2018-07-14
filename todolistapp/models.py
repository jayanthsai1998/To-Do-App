from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)

    def __str__(self):
        return "Todo List: " + self.name


class ToDoListItem(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    finished = models.BooleanField(default=False)
    date_created = models.DateField(default=now().date())