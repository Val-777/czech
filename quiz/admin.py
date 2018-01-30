from django.contrib import admin

from .models import Noun, Verb, PersPronoun, ExNNS, ExAAS, ExLNS, ExIIV, ExKKV


admin.site.register(Noun)
admin.site.register(Verb)
admin.site.register(PersPronoun)

admin.site.register(ExNNS)
admin.site.register(ExAAS)
admin.site.register(ExLNS)
admin.site.register(ExIIV)
admin.site.register(ExKKV)
