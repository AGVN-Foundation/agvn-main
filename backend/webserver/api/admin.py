from .models import User
from django.contrib import admin
from .models import Vote, Poll, Voter, Department, Residence, Country, Occupation
from .models import Initiative, Election, Policy, Skill, Interests

# Register your models here.
from .models import Voter, ElectedInitiative, ElectionResults, JobOffer, JobPromotion

admin.site.register(User)
admin.site.register(Voter)
admin.site.register(Vote)
admin.site.register(Poll)
admin.site.register(Department)
admin.site.register(Initiative)
admin.site.register(Election)
admin.site.register(Policy)
admin.site.register(Skill)
admin.site.register(Interests)
admin.site.register(Residence)
admin.site.register(Country)
admin.site.register(Occupation)
admin.site.register(ElectedInitiative)
admin.site.register(ElectionResults)
admin.site.register(JobPromotion)
admin.site.register(JobOffer)
