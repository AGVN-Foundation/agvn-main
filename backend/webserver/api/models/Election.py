from django.db import models


class Election(models.Model):
    elect_id = models.AutoField(primary_key=True, auto_created=True)
    # we only care about month and year
    # Assume elections are held at the first day of election month
    election_start = models.DateTimeField()
    # default -? elections end in a month. I.e. initiatives hav 1 month to campaign for their cause
    # and people can vote any time during that
    election_end = models.DateTimeField()
    is_active = models.BooleanField(default=True)
