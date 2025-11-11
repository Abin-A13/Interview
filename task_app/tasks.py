import time
import random
import traceback
from django.conf import settings
from django.core.cache import cache
from celery import shared_task
from task_app.models import Task
from task_app.serializers import TaskSerializer


@shared_task(bind=True, name="task_app.run_long_task_async")
def run_long_task_async(self, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return {"status": "not found"}

    try:
        task.status = "IN_PROGRESS"
        task.save()
        cache.set(f"task:{task_id}", TaskSerializer(
            task).data, settings.TASK_CACHE_TTL)
        seconds = random.randint(10, 20)
        for sec in range(seconds):
            time.sleep(1)
            try:
                self.update_state(state="PROGRESS", meta={
                                  "current": sec + 1, "total": seconds})
            except Exception:
                pass
        result = {
            "message": f"Processed task '{task.title}'",
            "processed_seconds": seconds,
        }
        task.status = "SUCCESS"
        task.result = result
        task.save()

        cache.set(f"task:{task_id}", TaskSerializer(
            task).data, settings.TASK_CACHE_TTL)
        return {"status": "success", "result": result}
    except Exception as exc:
        task.status = "FAILED"
        task.result = {"error": "Task failed", "details": str(exc)}
        task.save()
        cache.set(f"task:{task_id}", TaskSerializer(
            task).data, settings.TASK_CACHE_TTL)

        traceback.print_exc()
        raise
