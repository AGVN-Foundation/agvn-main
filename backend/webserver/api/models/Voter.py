'''
    Desc: Represents a voter in the AGVN. Everyone is a voter, except AGVN admins.
'''
from re import T
from typing import List
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
import uuid
from django.contrib.postgres.fields import ArrayField
from django.db.models.deletion import CASCADE

from .Education import Education
from .Sex import Sex
from .Residence import Residence
from .Country import Country
from .Occupation import Occupation
from .Skill import Skill
from .Interests import Interests
from django.contrib.postgres.fields import ArrayField
from .Policy import Policy_Type


class Voter(models.Model):
    '''
        - Residence is null if voter does not live in australia -> e.g. overseas PR.
        - user_id is generated using UUID to ensure it is unqiue, driver license is unique field
    '''
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    legal_name = models.CharField(max_length=50, default=None)
    sex = Sex
    age = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(150), MinValueValidator(18)], default=None)
    driver_license = models.CharField(max_length=8, validators=[
                                      RegexValidator(r'^\d{8}$')], default=None, unique=True)
    medicare = models.JSONField(default=dict)
    n_family = models.IntegerField(default=None, null=True)
    education_level = Education
    residence = models.ForeignKey(
        Residence, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(
        Country, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    current_occupation = models.ForeignKey(
        Occupation, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    # store job rank, e.g. level 4 teacher
    # default = 2
    occupation_rank = models.IntegerField(default=2, null=True)
    income = models.IntegerField()
    # voter is a government employee
    government_employee = models.BooleanField(default=False)

    # voter >--< skill
    skills = models.ManyToManyField(
        Skill, blank=True)
    # # voter >--< interest
    interests = models.ManyToManyField(
        Interests, blank=True)

    # stores a user's contribution up to 30 days
    contributions = ArrayField(
        models.PositiveIntegerField(), size=30, blank=True, null=True)

    # store a user's political
    political_interest = ArrayField(
        models.DecimalField(decimal_places=2, max_digits=3), size=17, blank=True, null=True)
    
    # store user's gcoin id
    gcoin_address = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.legal_name
