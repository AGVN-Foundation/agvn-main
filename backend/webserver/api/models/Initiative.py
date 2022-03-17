'''
Initiatives are abstractions of ideologies in real life.
Each initiative has their own value for each policy type.

The InitiativeTypes listed here are based on what we see in the current
state of Australian society.

In theory, there should not be any 'initiative types' and only the
automatic clustering of the mass sentiment for each policy type.
For now, this provides a decent abstraction of reality to represent.
'''
from django.db import models
from .Election import Election
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


class InitiativeType(models.IntegerChoices):
    # Referenced from the political leanings of Australian parties
    # NOTE: is not actually based on the 'political compass'
    # instead, refers to the 'policy type' values

    CONSERVATIVE = 1, ('Conservative')
    PROGRESSIVE = 2, ('Progressive')
    LIBERTARIAN = 3, ('Libertarian')
    ACTIVIST = 4, ('Activist')
    LEFT_LIBERTARIAN = 5, ('Left Libertarian')
    SOCIAL_DEMOCRATIC = 6, ('Social Democratic')
    STATIST = 7, ('Statist')
    AUTHORITARIAN = 8, ('Authoritarian')


class Initiative(models.Model):
    initiative_type = models.IntegerField(
        primary_key=True, choices=InitiativeType.choices)
    # one to many, election <- initiative
    election = models.ManyToManyField(
        Election, blank=True, default=None)
    # For now, simply have unique policies for each initiative initiatives >---< policies
    # an initiative can have many policies, e.g. 5
    # a policy can be owned by many initiatives, e.g. 2
    # policies = models.ManyToManyField(Policy)
    policy_type_weights = ArrayField(
        models.FloatField(), size=17)

    def __str__(self) -> str:
        return str(InitiativeType(self.initiative_type).label)