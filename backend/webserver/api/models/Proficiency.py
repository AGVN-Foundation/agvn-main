'''
    Desc: An enum class that represents a user's proficiency in ___.
'''
from django.db import models
from django.utils.translation import gettext_lazy as _


class _Proficiency(models.IntegerChoices):
    LOW = 1, _('Low/Familiar')
    MED = 2, _('Medium/Proficient')
    HIGH = 3, _('High/Expert')


Proficiency = models.IntegerField(choices=_Proficiency.choices)
