from django.db import models
from .User import User
from .Occupation import Occupation


class JobOffer(models.Model):
    '''
    Idea -> check what occupations are in demand (database of jobs in demand)
    If there is an occupation available that is not the voter's one,
    check if voter has income < 100,000
    If so, offer them this position (default_rank=2)
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_offer = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    job_rank = models.IntegerField(default=2)
