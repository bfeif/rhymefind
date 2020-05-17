import os, sys

proj_path = "."
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rhymefindersite.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from rhymefind.models import Word, RhymeCouplet, RhymeFind
from django.db.models import Func, F, Q
from tqdm import tqdm
import numpy as np


############
# LOAD THE RHYMEFIND table
# constants for index view
couplet_glove_names = ['glove_mean_' +
					   str(i) for i in range(32)]
word_glove_names = ['glove_' + str(i) for i in range(32)]
zipped_names = list(zip(couplet_glove_names, word_glove_names))
window_size = 2.5

def get_top_rcs(word):
	# build the filter box query arguments
	lt_filter_kwargs = {couplet_glove_name + '__gte': getattr(word, word_glove_name) - window_size / 2 for
						couplet_glove_name, word_glove_name in zipped_names}
	gt_filter_kwargs = {couplet_glove_name + '__lte': getattr(word, word_glove_name) + window_size / 2 for
						couplet_glove_name, word_glove_name in zipped_names}
	lt_filter_kwargs.update(gt_filter_kwargs)

	# do the box pre-query
	boxed_couplets = RhymeCouplet.objects.\
		filter(~Q(word1=word)).\
		filter(~Q(word2=word)).\
		filter(**lt_filter_kwargs)

	# now order the stuff in the box
	ordered_couplets = boxed_couplets.annotate(
		abs_diff=Func(
			sum([(F(couplet_glove_name) - getattr(word, word_glove_name))
							 ** 2 for couplet_glove_name, word_glove_name in zipped_names]),
			function='ABS'
		)).\
		order_by('abs_diff')
	length_all_results = len(ordered_couplets)
	result_length = min(15, length_all_results)
	top_couplets = ordered_couplets[:result_length]
	return length_all_results, top_couplets

# for each word, query
for word in tqdm(Word.objects.filter(is_english=True).all()):
	
	# get the top rhyme couplets
	len_all_results, top_couplets = get_top_rcs(word)

	# now store the rhymefinds to RhymeFind table
	for rc in top_couplets:
		rf = RhymeFind(
			find_distance=np.sqrt(rc.abs_diff),
			word=word,
			rhyme_couplet=rc,
			nsfw=False
			)
		rf.save()