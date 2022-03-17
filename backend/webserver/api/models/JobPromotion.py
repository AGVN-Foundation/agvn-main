from django.db import models
from .User import User
from .Occupation import Occupation


class JobPromotion(models.Model):
    '''
    Idea -> check user's current occupation and rank, add 1 to it.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    job_rank = models.IntegerField()
