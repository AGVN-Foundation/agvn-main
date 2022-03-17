from django.db import models
from .Election import Election
from django.contrib.postgres.fields import ArrayField


class ElectionResults(models.Model):
    '''
    Contain the results for a given election
    '''
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    # store raw percent data for each initiative
    n_votes_initiatives = ArrayField(models.IntegerField())
    initiative_names = ArrayField(models.TextField())
    # Add other demographics and data here
