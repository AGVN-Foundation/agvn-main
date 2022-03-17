from django.db import models
from .Policy import Policy_Type
from django.utils.translation import gettext_lazy as _

class PollType(models.IntegerChoices):
    MULTI_CHOICE = 1, _('Multiple Choices')
    SCALE = 2, _('Scale')
    SHORT_ANSWER = 3, _('Short Answer')
    CHECK_BOX = 4, _('Check Box')
    DROP_DOWN = 5, _('Drop Down')

class Poll(models.Model):
    '''
    @End dates can be e.g., current date + 7 days
        multiple choice, drop down, checkbox: a,b,c,d
        scale: "1,10" or "1,5"
        short answer: ""
    '''
    # Assume all questions are text, e.g. "What do you think about our Education budget this year?"
    # "Do you think something needs to be done for social issue X -> sentiment analysis"
    question = models.TextField()
    ongoing = models.BooleanField(default=False)
    type = models.IntegerField(choices=PollType.choices)
    end_date = models.DateField()
    possible_answers = models.TextField()
    subject = models.IntegerField(choices=Policy_Type.choices)
