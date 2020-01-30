from django.contrib import admin
from .models import RhymeCouplet, Glove, RhymeCouplet50d, Glove50d

admin.site.register(RhymeCouplet)
admin.site.register(Glove)
admin.site.register(RhymeCouplet50d)
admin.site.register(Glove50d)