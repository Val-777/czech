from rest_framework.generics import ListAPIView

from addwords.models import PersPronoun
from .serializers import PersPronounSerializer


class PersPronounListAPIView(ListAPIView):
    queryset = PersPronoun.objects.all()
    serializer_class = PersPronounSerializer
