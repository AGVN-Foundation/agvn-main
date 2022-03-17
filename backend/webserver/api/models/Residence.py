'''
    Desc: Holds the address of a user and electorial district.
'''
from django.db import models


class Residence(models.Model):
    '''
        # NOTE: using 'custom districts'.
        For federal electoral districts, use https://www.aec.gov.au/profiles/
        @fields: user, unit, street name, street type, suburb.
    '''
    address = models.CharField(max_length=150)
    suburb = models.CharField(max_length=150)
    postcode = models.IntegerField()
    # Formatted like 'DistrictName State'
    electoral_district = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.address + ", " + self.suburb + ", " + str(self.postcode)
