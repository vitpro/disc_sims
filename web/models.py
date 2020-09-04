from django.db import models


class Player(models.Model):
    hp = models.IntegerField()
