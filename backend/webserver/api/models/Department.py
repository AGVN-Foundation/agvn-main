from django.db import models
from polymorphic.models import PolymorphicModel
from .Policy import Policy_Type
from django.utils.translation import gettext_lazy as _


class DepartmentName(models.IntegerChoices):
    DEPARTMENT_HEALTH = 1, _('Department of Health')
    DEPARTMENT_EDUCATION = 2, _('Department of Education, Skills and Employment')
    DEPARTMENT_DEFENSE = 3
    DEPARTMENT_FOREIGN_AFFAIRS = 4
    DEPARTMENT_HOME_AFFAIRS = 5
    DEPARTMENT_INDUSTRY_SCIENCE = 6
    DEPARTMENT_INFRASTRUCTURE = 7
    DEPARTMENT_SOCIAL_SERVICE = 8
    DEPARTMENT_TREASURY = 9
    DEPARTMENT_VETERANS = 10
    DEPARTMENT_AGRICULTURE_ENVIRONMENT = 11
    DEPARTMENT_FINANCE = 12
    # Extension: Scrape this page: https://www.directory.gov.au/departments-and-agencies
    # and put them in a list, then use IntegerField(choices=list)


class Level(models.IntegerChoices):
    FEDERAL = 1, _('Fedral Parliament')
    STATE = 2, _('State/Territory Parliament')
    LOCAL = 3, _('Local Council')


class Department(PolymorphicModel):
    type = models.IntegerField(choices=Policy_Type.choices)
    name = models.IntegerField(choices=DepartmentName.choices)
    description = models.TextField()
    level = models.IntegerField(choices=Level.choices)


class StateDepartment(Department):
    state = models.CharField(max_length=5, default=None)


class LocalDepartment(Department):
    electoral_district = models.CharField(max_length=15, default=None)
