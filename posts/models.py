from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=256)
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title