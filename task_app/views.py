from django.core.cache import cache
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from task_app.models import Task
from task_app.tasks import run_long_task_async
from task_app.serializers import TaskSerializer

class TaskCreateView(APIView):
    permission_class = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task_obj  = Task.objects.create(
                title=serializer.validated_data['title'],
                owner=request.user
            )
            run_long_task_async.delay(task_obj.id)
            key = f"task:{task_obj.id}"
            cache.set(key, TaskSerializer(task_obj).data, settings.TASK_CACHE_TTL)
            return Response(TaskSerializer(task_obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListView(ListAPIView):
    serializer_classes = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self, request):
        qs = Task.objects.filter(owner=request.user).order_by("-created_at")
        status_param = self.request.query_params.get("status")
        from_date = self.request.query_params.get("from_date")
        to_date = self.request.query_params.get("to_date")
        if status_param:
            qs = qs.filter(status=status_param)
        if from_date:
            qs = qs.filter(created_at__gte=from_date)
        if to_date:
            qs = qs.filter(created_at__lte=to_date)
        return qs
    
class TaskRetrieveView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        cache_key = f"task:{pk}"
        cached = cache.get(cache_key)
        if cached:
            try:
                obj = Task.objects.get(id=pk)
            except Task.DoesNotExist:
                raise NotFound("Task not found")
            if obj.owner != request.user:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            return Response(cached)
        try:
            task = Task.objects.get(id=pk, owner=request.user)
        except Task.DoesNotExist:
            raise NotFound("Task not found")
        data = TaskSerializer(task).data
        cache.set(cache_key, data, settings.TASK_CACHE_TTL)
        return Response(data)

class TaskDeleteView(RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk):
        try:
            task = Task.objects.get(id=pk, owner=request.user)
        except Task.DoesNotExist:
            raise NotFound("Task not found")
        cache_key = f"task:{pk}"
        task.delete()
        cache.delete(cache_key)
        return Response(status=status.HTTP_204_NO_CONTENT)


