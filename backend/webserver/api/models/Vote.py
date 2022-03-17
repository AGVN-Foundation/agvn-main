from django.db import models
from .Election import Election
from django.contrib.postgres.fields import ArrayField
from .User import User
from .Initiative import InitiativeType


class Vote(models.Model):
    # NOTE: cascade -> when election is deleted, all votes for that election is deleted
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    # variable number of initiatives
    initiatives = ArrayField(models.IntegerField(choices=InitiativeType.choices))
