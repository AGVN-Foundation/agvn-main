from .Initiative import Initiative
from django.db import models
from django.utils.translation import gettext_lazy as _


class Policy_Type(models.IntegerChoices):
    '''
    Using the following as guidelines
    https://allnewaustralia.com/political-issues/list-of-australian-political-issues
    '''
    TAXATION = 1, _('Taxation')
    LIFESTYLE_CULTURE = 2, _('Lifestyle Culture')
    COMMUNITY = 3, _('Community')
    INFRASTRUCTURE = 4, _('Infrastructure')
    FOREIGN_RELATIONS = 5, _('Foreign Relations')
    HEALTH = 6, _('Health')
    EDUCATION_EMPLOYMENT = 7, _('Education Employment')
    NATIONAL_SECURITY = 8, _('National Security')
    SAFETY = 9, _('Safety')
    INDUSTRY = 10, _('Industry')
    SCIENCE_TECHNOLOGY = 11, _('Science/Technology')
    ENVIRONMENT = 12, _('Environment')
    ENERGY = 13, _('Energy')
    ASSETS = 14, _('Assets')
    ECONOMY = 15, _('Economy')
    FOREIGN_TRADE = 16, _('Foreign Trade')
    NATURAL_RESOURCES = 17, _('Natural Resources')


class Policy(models.Model):
    '''
    Should contain a single policy, like a civ6 policy card
    Contains: type of policy, description of policy -> using GPT

    @policy_cost, a number between -MAX_BUDGET, MAX_BUDGET
    '''
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE)
    policy_type = models.IntegerField(choices=Policy_Type.choices)
    policy_title = models.TextField()
    policy_description = models.TextField()
    policy_cost = models.FloatField()

    def __str__(self) -> str:
        return str(Policy_Type(self.policy_type).label)
