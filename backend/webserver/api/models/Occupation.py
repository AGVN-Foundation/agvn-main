'''
    Desc: An occupation of a user, contains their position and description
'''
from django.db import models
from polymorphic.models import PolymorphicModel
from .User import User
from .Policy import Policy
from django.utils.translation import gettext_lazy as _


# Extension for later -> user value only
# class Position(models.IntegerChoices):
#     VOLUNTEER = 1
#     INTERN = 2
#     JUNIOR = 3
#     EXPERIENCED = 4
#     SENIOR = 5
#     MANAGEMENT = 6
#     EXECTIVE = 7


'''
IDEA of Occupation type
https://joboutlook.gov.au/industries/
Agriculture, Forestry, Fishing -> Industry
Mining -> Industry
Manufacturing -> Industry
Electricity, Gas, Water, Waste Services -> Environment, Industry
Construction -> Industry
Wholesale trade -> Economics
Retail trade -> Economics
Accomodation and Food services -> Economics
Transport, Postal, Warehousing -> Infrastructure
Information media, Telecommunications -> Community
Financial, insurance services -> Economics
Rental, hiring and real estate services -> Economics
Professional, scientific and technical services -> Science
Administrative, support services -> Community
Public administration, safety -> Safety, Public service
Education, training -> Education, Employment
Healthcare, social assistance -> Health
Arts, Recreation services -> Lifestyle
'''


class OccupationType(models.IntegerChoices):
    ENVIRONMENTAL_INDUSTRY = 1, _('Environmental Industry')
    MINING = 2, _('Mining')
    MANUFACTURING = 3, _('Manufacturing')
    UTILITIES = 4, _('Utilities')
    CONSTRUCTION = 5, _('Construction')
    WHOLESALE_TRADE = 6, _('Wholesale Trade')
    RETAIL_TRADE = 7, _('Retail Trade')
    ACCOMODATION_FOOD = 8, _('Accomodation Food')
    LOGISTICS = 9, _('Logistics')
    MEDIA = 10, _('Media')
    FINANCIAL = 11, _('Financial')
    REAL_ESTATE = 12, _('Real Estate')
    PROFESSIONAL_SCIENTIFIC = 13, _('Professional Scientific')
    ADMINISTRATIVE_SUPPORT = 14, _('Administrative Support')
    PUBLIC_ADMINISTRATION_SAFETY = 15, _('Public Administration Safety')
    EDUCATION_TRAINING = 16, _('Education Training')
    HEALTHCARE_SOCIAL = 17, _('Healthcare Social')
    ARTS_RECREATION = 18, _('Arts Recreation')

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Occupation(PolymorphicModel):
    """
    NOTE: assume A-GVN has access to tax data, which contains the user's current occupation.
    Also assume that users do not frequently change their occupation or position, so everything updates accurately every financial year.

    @fields Contains user id int, description text, demand_level int fields.
    demand_level -> any integer. Basically an index. The more positive the demand level, the higher it is in demand.
    """
    type = models.IntegerField(choices=OccupationType.choices, default=None)
    description = models.TextField()
    demand_level = models.IntegerField()
    
    def __str__(self) -> str:
        return str(OccupationType(self.type).label)
    
