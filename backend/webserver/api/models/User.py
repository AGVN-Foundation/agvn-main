from django.db import models
'''
    Desc: This class represents the users' account information and is the super
    class of the different types of AGVN users; eg. Voters, AGVNAdmins, etc.
'''
MAX_EMAIL_LEN = 150


class User(models.Model):
    '''
        Class Constructor takes user_id, email, & password.
        NOTE: django recommends class methods to instantiate models.
    '''
    user_id = models.UUIDField(primary_key=True, default=None, unique=True)
    email = models.EmailField(unique=True)
    hashed_password = models.CharField(max_length=100)
    def __str__(self):
      return self.email