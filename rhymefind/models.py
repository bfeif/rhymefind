from django.db import models
from django.contrib.postgres.fields import ArrayField

'''
NOTE: DJANGO does not actually update the schema of the db when you add a default value to a column
'''

max_length=100

# rhyme couplet glove model
class RhymeCouplet(models.Model):

    # fields to add
    date_added = models.DateField(auto_now_add=True)
    date_last_updated = models.DateField(auto_now=True)
    nsfw = models.BooleanField(default=False)
    
    # fields from Python model
    word_1 = models.CharField(max_length=max_length)
    word_2 = models.CharField(max_length=max_length)
    phoneme_seq_1 = ArrayField(models.CharField(max_length=3), null=True)
    phoneme_seq_2 = ArrayField(models.CharField(max_length=3), null=True)
    rhyme_seq = ArrayField(models.CharField(max_length=3), null=True)

    # method definition
    def __str__(self):
        return (self.word_1 + ', ' + self.word_2)


# add glove attributes to RhymeCouplet
for i in range(100):
    RhymeCouplet.add_to_class('glove_mean_' + str(i), models.FloatField(null=True))


# single word glove model
class Glove(models.Model):
    word = models.CharField(max_length=max_length)
    nsfw = models.BooleanField(default=False)

    # method definition
    def __str__(self):
        return (self.word)


# add glove attributes to RhymeCouplet
for i in range(100):
    Glove.add_to_class('glove_' + str(i), models.FloatField(null=True))