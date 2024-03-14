from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True, null=True)  # Допускает NULL значения
    subscribers = models.ManyToManyField(User, verbose_name='Подписчики', related_name='subscribed_topics', blank=True)


class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question_text = models.TextField()
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)

class Word(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    word_text = models.CharField(max_length=255)
    word_translate = models.TextField()
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)

class Answer(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()


