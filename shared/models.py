from django.utils import timezone

from django.db import models

from users.models import CustomUser


class FeedBackModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="feedback")
    title = models.CharField(max_length=70, )
    body = models.TextField(max_length=300, null=True, blank=True)
    publish_time = models.DateTimeField(default=timezone.now)

class MurojaatModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="murojaat")
    title = models.CharField(max_length=70, )
    body = models.TextField(max_length=300, null=True, blank=True)
    publish_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username.title()}dan -> {self.title}"
