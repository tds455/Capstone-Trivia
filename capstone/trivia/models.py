from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Userstats(models.Model):
    userid = models.IntegerField()
    score = models.IntegerField()
    gamesplayed = models.IntegerField()

class IDcache(models.Model):
    category = models.CharField(max_length=20)
    APIID = models.IntegerField()