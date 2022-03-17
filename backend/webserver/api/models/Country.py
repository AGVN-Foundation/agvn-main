'''
    Desc: Represents a country and if they are on friendly terms with Australia.
'''
from django.db import models
from .User import User


class Country(models.Model):
    '''
        Fields include a country's name and whether they're
        on friendly terms.
        For internal use only. Impossible for someone to 'change' their background.
    '''
    country = models.CharField(max_length=60)
    friendly_terms = models.BooleanField()

    @classmethod
    def update_friendly_terms(self, country, friendly_terms: bool):
        '''
        Setter for friendly_terms, updates the relationship between a country and Australia.
        Used for user editing logic.
        '''
        try:
            c = Country.objects.get(country=country)
            c.friendly_terms = friendly_terms
        except Exception as e:
            print("Error:", e)
    
    def __str__(self):
      return self.country