from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher')
    title = models.CharField('Title', max_length=100)
    question = models.TextField('Question')
    answer = models.TextField(default=None, null=True, blank=True)
    status = models.TextField(default='Not read yet', null=True, blank=True, )
    isDone = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ('-id',)
