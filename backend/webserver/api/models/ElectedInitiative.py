from django.db.models.deletion import CASCADE
from .Initiative import Initiative
from django.db import models


class ElectedInitiative(models.Model):
    '''
    There should only be one elected initiative.
    '''
    elected_initiative = models.ForeignKey(Initiative, on_delete=CASCADE)
