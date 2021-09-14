from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Func, F, Q
from datetime import datetime
max_length = 100
couplet_glove_names = ['glove_mean_' +
                       str(i) for i in range(32)]
word_glove_names = ['glove_' + str(i) for i in range(32)]
zipped_names = list(zip(couplet_glove_names, word_glove_names))
window_size = 2.5

'''
NOTE: DJANGO does not actually update the schema of the db when you add a default value to a column
'''


class Word(models.Model):

    word = models.CharField(max_length=max_length, db_index=True, unique=True)
    phoneme_seq = ArrayField(models.CharField(max_length=3), null=True)
    rhyme_seq = ArrayField(models.CharField(max_length=3), null=True)
    is_english = models.BooleanField(default=False)
    num_finds = models.IntegerField(default=0)

    class Meta:
        unique_together = (('word', 'phoneme_seq'),)
        indexes = [
            models.Index(fields=['word'], name="Word_word_idx")
        ]

    def __str__(self):
        return '{word}'.format(word=self.word, phoneme_seq=self.phoneme_seq)

    def find_rhymes(self):
        return RhymeFind.objects.filter(word=self)

    def find_rhymes_deep(self, window_size=2.5):
        # build the filter box query arguments
        lt_filter_kwargs = {couplet_glove_name + '__gte': getattr(self, word_glove_name) - window_size / 2 for
                            couplet_glove_name, word_glove_name in zipped_names}
        gt_filter_kwargs = {couplet_glove_name + '__lte': getattr(self, word_glove_name) + window_size / 2 for
                            couplet_glove_name, word_glove_name in zipped_names}
        lt_filter_kwargs.update(gt_filter_kwargs)

        # do the box pre-query
        boxed_couplets = RhymeCouplet.objects.\
            filter(~Q(word1=self)).\
            filter(~Q(word2=self)).\
            filter(**lt_filter_kwargs)

        # now order the stuff in the box
        ordered_couplets = boxed_couplets.annotate(
            abs_diff=Func(
                sum([(F(couplet_glove_name) - getattr(self, word_glove_name))
                                 ** 2 for couplet_glove_name, word_glove_name in zipped_names]),
                function='ABS'
            )).\
            order_by('abs_diff')
        length_all_results = len(ordered_couplets)
        result_length = min(15, length_all_results)
        top_couplets = ordered_couplets[:result_length]
        return top_couplets


for i in range(32):
    Word.add_to_class('glove_' + str(i), models.FloatField(null=True))


class RhymeCouplet(models.Model):
    word1 = models.ForeignKey(
        Word, related_name='word1', on_delete=models.CASCADE, db_index=True)
    word2 = models.ForeignKey(
        Word, related_name='word2', on_delete=models.CASCADE, db_index=True)

    class Meta:
        unique_together = (('word1', 'word2'),)
        indexes = [
            models.Index(fields=['word1', 'word2'], name="RC_wordpair_idx"),
            models.Index(fields=['word1'], name="RC_word1_idx"),
            models.Index(fields=['word2'], name="RC_word2_idx")
        ] + [models.Index(fields=['glove_mean_{}'.format(i)], name='RC_glove_mean_{}_idx'.format(i)) for i in range(32)]

    def __str__(self):
        return '{word1} {word2}'.format(word1=self.word1, word2=self.word2)


for i in range(32):
    RhymeCouplet.add_to_class(
        'glove_mean_' + str(i), models.FloatField(null=True))


class RhymeFind(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, db_index=True)
    rhyme_couplet = models.ForeignKey(RhymeCouplet, on_delete=models.CASCADE, db_index=True)
    nsfw = models.BooleanField(default=False)
    find_distance = models.FloatField(null=True)

    class Meta:
        unique_together = (('word', 'rhyme_couplet'),)
        indexes = [
            models.Index(fields=['word'], name='RF_word_idx')
        ]

    def __str__(self):
        return '{word}: {couplet}'.format(word=self.word, couplet=str(self.rhyme_couplet))


class Upvote(models.Model):
    rhymefind = models.ForeignKey(RhymeFind, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)
    up = models.BooleanField()

    def __str__(self):
        vote = '+1' if self.up else '-1'
        return '{up}: {rf}, {date}'.format(up=vote, rf=str(self.rhymefind), date=self.date)
