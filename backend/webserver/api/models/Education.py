from django.db import models
from django.utils.translation import gettext_lazy as _

'''
  Desc: An enum class that represents a user's education level
  according to the Australian Qualifications Framework (AQF)
'''

class _Education(models.IntegerChoices):
  Level0 = 0, _('N/A')
  Level1 = 1, _('Certificate I')
  Level2 = 2, _('Certificate II')
  Level3 = 3, _('Certificate III')
  Level4 = 4, _('Certificate IV')
  Level5 = 5, _('Diploma')
  Level6 = 6, _('Advanced Diploma, Associate Degree')
  Level7 = 7, _('Bachelor Degree')
  Level8 = 8, _('Bachelor Honours Degree, Graduate Certificate, Graduate Diploma')
  Level9 = 9, _('Masters Degree')
  Level10 = 10, _('Doctoral Degree')

Education = models.IntegerField(choices=_Education.choices)