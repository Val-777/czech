from rest_framework.generics import ListAPIView

from addwords.models import PersPronoun


class PersPronounListAPIView(ListAPIView):
    queryset = PersPronoun.objects.all()
