from django.contrib import admin

from .models import Noun, ExNNS, ExAAS


admin.site.register(Noun)

admin.site.register(ExNNS)
admin.site.register(ExAAS)
