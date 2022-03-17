'''
    Desc: Represent a skill of a user.
    NOTE: Basically the past occupations and experiences of a user
'''
from .Proficiency import Proficiency
from django.db import models
from .User import User
from polymorphic.models import PolymorphicModel
from .Occupation import OccupationType


class Skill(PolymorphicModel):
    type = models.IntegerField(choices=OccupationType.choices, default=None)
    description = models.TextField()
    
    def __str__(self):
      return str(OccupationType(self.type).label)
