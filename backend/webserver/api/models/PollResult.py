from django.db import models
from .Poll import Poll
from .User import User


class PollResult(models.Model):
    '''
    Infer answer type from poll type
    '''
    # primary key = (question_id, user_id)
    question_id = models.ForeignKey(
        Poll, on_delete=models.CASCADE, default=None, blank=True, null=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    date_time = models.DateTimeField()
    answer = models.TextField()

    class Meta:
        unique_together = ['question_id', 'user_id']
