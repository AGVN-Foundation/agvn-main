'''
    Possible benefits -> delivered with GCoin transaction/notice from AGVN
    For now, AGVN will send an email to users who are eligible for benefits on a daily basis (tick)
    Contains tiers 1-3 in terms of amounts and value
    For now, the server does a simple check for the types of benefits available
'''
from django.db import models


class ContributionBenefits(models.Model):
    amount = models.IntegerField()
    benefit = models.TextField(default=None, null=True)
