from django.db import models
from django.contrib.postgres.fields import ArrayField


# rhyme couplet glove model
class RhymeCouplet(models.Model):
    
    # fields to add
    date_added = models.DateField(auto_now_add=True)
    date_last_updated = models.DateField(auto_now=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    nsfw = models.BooleanField(default=False)
    
    # fields from Python model
    word_1 = models.CharField(max_length=30)
    word_2 = models.CharField(max_length=30)
    phoneme_seq_1 = ArrayField(models.CharField(max_length=3), null=True)
    phoneme_seq_2 = ArrayField(models.CharField(max_length=3), null=True)
    rhyme_seq = ArrayField(models.CharField(max_length=3), null=True)
    # glove = ArrayField(models.FloatField())


# add glove attributes to RhymeCouplet
for i in range(100):
    RhymeCouplet.add_to_class('glove_mean_' + str(i), models.FloatField(null=True))


# single word glove model
class Glove(models.Model):
    word = models.CharField(max_length=30)
    nsfw = models.BooleanField(default=False)
    # glove = ArrayField(models.FloatField())


# add glove attributes to RhymeCouplet
for i in range(100):
    Glove.add_to_class('glove_' + str(i), models.FloatField(null=True))
