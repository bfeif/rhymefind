# imports
from django.http import HttpResponse
from django.template import loader
from .models import Word

# Configure logger
import logging
logger = logging.getLogger(__name__)
GLOVE_DIMENSIONS = 32
fun_words = ['pirate', 'paper', 'marriage', 'believe', 'feed', 'america', 'indigenous', 'radical', 'coup', 'feast', 'archaeologist', 'blunt',
             'leader', 'raft', 'trade', 'newspaper', 'piano', 'flagrant', 'manager', 'football', 'nonsense', 'prostitute', 'computer']


def index(request):

    if request.method == 'GET':

        # get the query from the search box
        query_word = request.GET.get('search_box')
        logger.debug('query_word is "{}"'.format(query_word))
        if query_word:
            query_word = query_word.strip().lower()

        # run the query
        try:

            # get the Word object
            found_word = Word.objects.get(word=query_word)
            logger.debug(
                'found_word for rhyme couplet lookup is "{}"'.format(found_word))
            top_rhymefinds = list(found_word.find_rhymes().order_by('find_distance'))

        except Word.DoesNotExist:

            # if the Glove32dIND does not exist
            logger.debug(
                'No word found for query word "{}"'.format(query_word))
            found_word = None
            top_rhymefinds = None

    template = loader.get_template('rhymefind/index.html')
    context = {'rhymefinds': top_rhymefinds,
               'found_word': found_word, 'fun_words': fun_words}
    return HttpResponse(template.render(context, request))
