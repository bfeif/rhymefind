# imports
from django.http import HttpResponse
from django.template import loader
from .models import RhymeCouplet, Glove
from django.db.models import Func, F, Q

# Configure logger
import logging
logger = logging.getLogger(__name__)


def index(request):

	couplet_glove_names = ['glove_mean_'+str(i) for i in range(100)]
	word_glove_names = ['glove_'+str(i) for i in range(100)]
	zipped_names = zip(couplet_glove_names, word_glove_names)

	if request.method == 'GET':
		query_word = request.GET.get('search_box')
		logger.debug('query_word is "{}"'.format(query_word))
		try:
			found_word = Glove.objects.get(word=query_word)
			logger.debug('found_word for rhyme couplet lookup is "{}"'.format(found_word))
			couplets = RhymeCouplet.objects.\
				filter(~Q(word_1=found_word.word)).\
				filter(~Q(word_2=found_word.word)).\
				annotate(
					abs_diff=Func(
						sum([(F(couplet_glove_name) - getattr(found_word, word_glove_name))**2 for couplet_glove_name, word_glove_name in zipped_names]), 
						function='ABS'
					)).\
				order_by('abs_diff')[:5]
			logger.debug('rhyme couplets found for {found_word} are {couplets}'.format(found_word=found_word, couplets=couplets))
		except Glove.DoesNotExist:
			logger.debug('No word found for query word "{}"'.format(query_word))
			found_word = None
			couplets = None
	template = loader.get_template('rhymefind/index.html')
	context = {'couplets': couplets, 'found_word': found_word}
	return HttpResponse(template.render(context, request))
