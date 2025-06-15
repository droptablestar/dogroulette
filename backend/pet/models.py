from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=50, blank=True, default="")
    gender = models.CharField(max_length=50, blank=True, default="")
    size = models.CharField(max_length=50, blank=True, default="")
    breed = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")
    photos = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=50, blank=True, default="")
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
