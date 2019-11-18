from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.conf import settings
from django.db.models import signals


class Post(models.Model):
    title = models.CharField(max_length=256)
    content = RichTextUploadingField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def save(self,*args, **kwargs):
        if self.author.is_editor or self.author.is_staff:
            self.is_active = True
        super().save(*args, **kwargs)
        


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - {}".format(self.author, self.content)


def comment_post_save(sender, instance, signal, *args, **kwargs):
    from posts.tasks import send_comment_notifier
    send_comment_notifier.delay(instance.pk)


signals.post_save.connect(comment_post_save, sender=Comment)