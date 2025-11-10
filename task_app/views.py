from rest_framework import viewsets
from task_app.models import Task
from task_app.serializer import TaskSerializer

class TaskView(viewsets.ModelViewSet):
    querset=Task.objects.all()
    serializer_class = TaskSerializer


