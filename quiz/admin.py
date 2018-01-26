from django.contrib import admin

from .models import Noun, Verb, ExNNS, ExAAS, ExLNS


admin.site.register(Noun)
admin.site.register(Verb)

admin.site.register(ExNNS)
admin.site.register(ExAAS)
admin.site.register(ExLNS)
