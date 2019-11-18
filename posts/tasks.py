from news.celery import app
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from .models import Comment

@app.task
def send_comment_notifier(comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if comment:
        message = render_to_string('email/comment_email_notifier.html', {
                    'receiver': comment.post.author,
                    'domain': 'localhost:8000',
                    'post_url': comment.post.pk,
                    'post_title': comment.post.title
                })
        subject = "{} commented your post on NEWS".format(comment.author.email)
        email = EmailMessage(subject, message, to=[comment.post.author.email])
        email.send()
