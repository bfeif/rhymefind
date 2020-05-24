from django.contrib import admin
from .models import Word, RhymeCouplet, RhymeFind, Upvote

admin.site.register(Word)
admin.site.register(RhymeCouplet)
admin.site.register(RhymeFind)
admin.site.register(Upvote)