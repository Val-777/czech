from django.contrib import admin

from .models import Noun, Verb, PersPronoun

admin.site.register(Noun)
admin.site.register(Verb)
admin.site.register(PersPronoun)
