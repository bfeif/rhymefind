from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import RhymeCouplet, Glove
from django.views import View, generic


def index(request):

	words = Glove.objects.order_by('word')[:30]
	if request.method == 'GET':
		try:
			search_word = request.GET.get('search_box')
			found_glove = Glove.objects.get(word=search_word)
			print('bandana jack')
		except Glove.DoesNotExist:
			found_glove = None
	template = loader.get_template('rhymefind/index.html')
	context = {'words': words, 'found_glove': found_glove}
	return HttpResponse(template.render(context, request))