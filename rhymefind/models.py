from django.db import models
from django.contrib.postgres.fields import ArrayField


# rhyme couplet glove model
class RhymeCouplet(models.Model):
    word_1 = models.CharField(max_length=30)
    word_2 = models.CharField(max_length=30)
    date_added = models.DateField(auto_now_add=True)
    date_last_updated = models.DateField(auto_now=True)
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()
    nsfw = models.BooleanField()
    glove = ArrayField(models.FloatField())


# single word glove model
class Glove(models.Model):
    word = models.CharField(max_length=30)
    nsfw = models.BooleanField()
    glove = ArrayField(models.FloatField())
