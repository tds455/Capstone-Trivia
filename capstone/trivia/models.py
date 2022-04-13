from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Userstats(models.Model):
    userid = models.IntegerField()
    score = models.IntegerField(default = 0)
    gamesplayed = models.IntegerField(default = 0)
    artrating = models.IntegerField(default = 0)
    animalrating = models.IntegerField(default = 0)
    worldrating = models.IntegerField(default = 0)
    sportsrating = models.IntegerField(default = 0)
    movierating = models.IntegerField(default = 0)

    def serialise(self):
        return {
            "score": self.score,
            "artrating": self.artrating,
            "animalrating": self.animalrating,
            "worldrating": self.worldrating,
            "sportsrating": self.sportsrating,
            "movierating": self.movierating,
            "gamesplayed": self.gamesplayed
        }

class IDcache(models.Model):
    category = models.CharField(max_length=20)
    APIID = models.IntegerField()
    