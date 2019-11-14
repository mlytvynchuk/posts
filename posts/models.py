from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=256)
    content = RichTextUploadingField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk': self.pk})