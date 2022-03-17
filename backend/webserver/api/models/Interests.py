from django.db import models
from .User import User
from polymorphic.models import PolymorphicModel
from django.utils.translation import gettext_lazy as _



class _Level(models.IntegerChoices):
    LIKE = 1
    ENTHUSIAST = 2
    OBSSESSED = 3


class InterestType(models.IntegerChoices):
    # NOTE: can scrape from https://en.wikipedia.org/wiki/List_of_hobbies div class="div-col" then read it into here as a list of strings
    # try to group certain hobbies as the following, i.e. JSON object

    SPORTS = 1, _('Sports')
    SOCIAL = 2, _('Social')
    MEDIA = 3, _('Media')
    FASHION = 4, _('Fashion')
    ART_CRAFT_DIY = 5, _('Art, Craft, DIY')
    TRAVEL_OUTDOOR = 6, _('Travel, Outdoor')
    GAMING = 7, _('Gaming')
    LIFESTYLE = 8, _('LifeStyle')
    FOOD = 9, _('Food')
    AUTOMOTIVE = 10, _('Automotive')
    AGRICULTURAL_ACTIVITIES = 11, _('Agricultural Activities')
    RELGIOUS_SPIRITUAL = 12, _('Religious Spiritual')
    ANIMALS_PETS = 13, _('Animals/Pets')
    HEALTHY_EXERCISE = 14, _('Healthy Exercise')
    SCIENCE_TECHNOLOGY = 15, _('Science Technology')
    FINE_MANIPULATION = 16, _('Fine Manipulation')
    HOME_INDOOR = 17, _('Home/Indoor')
    EDUCATION = 18, _('Education')
    NICHE_INTERESTS = 19, _('Niche Interests')


class Interests(PolymorphicModel):
    type = models.IntegerField(choices=InterestType.choices, default=None)
    description = models.TextField()
    
    def __str__(self):
      return str(InterestType(self.type).label)