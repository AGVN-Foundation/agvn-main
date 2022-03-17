from .Policy import Policy_Type
from django.db import models
from django.contrib.postgres.fields import ArrayField


class Sentiment(models.Model):
    '''
    Represents the sentiment for each policy type

    @policy_type -> 1-17
    @strength -> 1-10
    '''
    policy_type = models.IntegerField(choices=Policy_Type.choices)
    strength = ArrayField(models.FloatField())
