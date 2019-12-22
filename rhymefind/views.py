from django.http import HttpResponse
from django.template import loader
from .models import RhymeCouplet, Glove
from django.db.models import Func, F



def index(request):

	if request.method == 'GET':
		try:
			query_word = request.GET.get('search_box')
			found_word = Glove.objects.get(word=query_word)
			couplets = RhymeCouplet.objects.annotate(abs_diff=Func(F('glove_mean_1') - found_word.glove_1, function='ABS')).order_by('abs_diff')[:5]
		except Glove.DoesNotExist:
			found_word = None
			couplets = None
	template = loader.get_template('rhymefind/index.html')
	context = {'couplets': couplets, 'found_word': found_word}
	return HttpResponse(template.render(context, request))