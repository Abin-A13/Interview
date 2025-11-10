from rest_framework.serializer import Serializer
from task_app.models import Task

class TaskSerializer(Serializer.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "status", "created_at", "updated_at", "result")
        read_only_fields = ("id", "status", "created_at", "updated_at", "result")