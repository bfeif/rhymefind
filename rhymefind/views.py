# imports
from django.http import HttpResponse
from django.template import loader
from .models import RhymeCouplet32dIND, Glove32dIND
from django.db.models import Func, F, Q
import time

# Configure logger
import logging
logger = logging.getLogger(__name__)
GLOVE_DIMENSIONS = 32
fun_words = ['pirate', 'paper', 'marriage', 'believe', 'feed', 'america', 'indigenous', 'radical', 'coup', 'feast', 'archaeologist', 'blunt',
             'leader', 'raft', 'trade', 'newspaper', 'piano', 'flagrant', 'manager', 'football', 'nonsense', 'prostitute', 'computer']


def index(request):

    # constants for index view
    couplet_glove_names = ['glove_mean_' +
                           str(i) for i in range(GLOVE_DIMENSIONS)]
    word_glove_names = ['glove_' + str(i) for i in range(GLOVE_DIMENSIONS)]
    zipped_names = list(zip(couplet_glove_names, word_glove_names))
    window_size = 3

    if request.method == 'GET':

        # get the query from the search box
        query_word = request.GET.get('search_box')
        logger.debug('query_word is "{}"'.format(query_word))
        if query_word:
            query_word = query_word.strip().lower()

        # run the query
        try:

            # get the Glove32dIND object
            t0 = time.time()
            found_word = Glove32dIND.objects.get(word=query_word)
            logger.debug(
                'found_word for rhyme couplet lookup is "{}"'.format(found_word))

            # build the filter box query arguments
            lt_filter_kwargs = {couplet_glove_name + '__gte': getattr(found_word, word_glove_name) - window_size / 2 for
                                couplet_glove_name, word_glove_name in zipped_names}
            gt_filter_kwargs = {couplet_glove_name + '__lte': getattr(found_word, word_glove_name) + window_size / 2 for
                                couplet_glove_name, word_glove_name in zipped_names}
            lt_filter_kwargs.update(gt_filter_kwargs)

            # run the query
            t1 = time.time()
            boxed_couplets = RhymeCouplet32dIND.objects.\
                filter(~Q(word_1=found_word.word)).\
                filter(~Q(word_2=found_word.word)).\
                filter(**lt_filter_kwargs)
            t2 = time.time()
            ordered_couplets = boxed_couplets.annotate(
                abs_diff=Func(
                    sum([(F(couplet_glove_name) - getattr(found_word, word_glove_name))
                         ** 2 for couplet_glove_name, word_glove_name in zipped_names]),
                    function='ABS'
                )).\
                order_by('abs_diff')
            top_couplets = ordered_couplets[:10]
            t3 = time.time()
            logger.debug('rhyme couplets found for {found_word} are {couplets}'.format(
                found_word=found_word, couplets=top_couplets))

            # show timing results
            print(t3 - t0)

        except Glove32dIND.DoesNotExist:

            # if the Glove32dIND does not exist
            logger.debug(
                'No word found for query word "{}"'.format(query_word))
            found_word = None
            top_couplets = None

    template = loader.get_template('rhymefind/index.html')
    context = {'couplets': top_couplets,
               'found_word': found_word, 'fun_words': fun_words}
    return HttpResponse(template.render(context, request))
