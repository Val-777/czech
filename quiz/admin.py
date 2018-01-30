from django.contrib import admin

from .models import ExNNS, ExAAS, ExLNS, ExIIV, ExKKV

admin.site.register(ExNNS)
admin.site.register(ExAAS)
admin.site.register(ExLNS)
admin.site.register(ExIIV)
admin.site.register(ExKKV)
