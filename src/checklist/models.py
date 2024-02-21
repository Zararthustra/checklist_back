from django.db import models
from django.conf import settings
import uuid


class Category(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=50, null=True)
    isHidden = models.BooleanField(default=False)
    isRecurrent = models.BooleanField(default=False)


class Task(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    isDisabled = models.BooleanField(default=False)
