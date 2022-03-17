# Put imports here.
from django.db import models
from django.utils.translation import gettext_lazy as _

'''
    Desc: An enum class that represents a user's gender.
'''


class _Sex(models.IntegerChoices):
    MALE = 1, _('Male')
    FEMALE = 2, _('Female')
    OTHER = 3, _('Indeterminate/Intersex/Unspecific')

# NOTE: apparently might need to specificy alias
Sex = models.IntegerField(choices=_Sex.choices)
