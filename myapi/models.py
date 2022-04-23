from operator import mod
from django.db.models.deletion import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from wordle_golf import settings


User = settings.AUTH_USER_MODEL

# Create your models here.


class Score(models.Model):
    game_number = models.IntegerField()
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" % (self.game_number, self.score, self.user)


class GolfGroup(models.Model):
    group_name = models.CharField(max_length=50)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.group_name


class User(AbstractUser):
    phone_number = models.CharField(max_length=12)
