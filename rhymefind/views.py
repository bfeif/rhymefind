from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import RhymeCouplet, Glove


def index(request):
    gloves = Glove.objects.order_by('word')[:30]
    template = loader.get_template('rhymefind/index.html')
    context = {'gloves': gloves}
    return HttpResponse(template.render(context, request))
