# Put imports here.
from .Country import Country

'''
    Desc: Creates an new instance of a country if an instance of said country
    has not been created. Since many users with have the same country, it would
    be redundant to have multiple instances of the same country.
'''


class CountryFactory:

    instances = {}      # class variable shared by all instances

    '''
        Class Constructor, no parameters needed
    '''

    def __init__(self):

        super().__init__()

    '''
        Creates a new instance a country if an instance of that country does not
        already exists, then returns the instance of the country.
    '''

    def create_country(self, country: str, friendly_terms: bool) -> Country:

        if country not in self.instances:
            self.instances[country] = Country(country, friendly_terms)
        return self.instances[country]

    '''
        Updates the relationship of a given country and Australia.
    '''

    def update_friendly_terms(self, country: str, friendly_terms: bool):

        if country in self.instances:
            self.instances[country].updade_friendly_terms(friendly_terms)
