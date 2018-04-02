from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)

from addwords.models import PersPronoun
from .serializers import (
    PersPronounSerializer,
    PersPronounCreateSerializer,
)


class PersPronounCreateAPIView(CreateAPIView):
    queryset = PersPronoun.objects.all()
    serializer_class = PersPronounCreateSerializer


class PersPronounListAPIView(ListAPIView):
    queryset = PersPronoun.objects.all()
    serializer_class = PersPronounSerializer


class PersPronounUpdateAPIView(UpdateAPIView):
    queryset = PersPronoun.objects.all()
    serializer_class = PersPronounSerializer


class PersPronounDeleteAPIView(DestroyAPIView):
    queryset = PersPronoun.objects.all()
    serializer_class = PersPronounSerializer


class PersPronounDetailAPIView(RetrieveAPIView):
    queryset = PersPronoun.objects.all()
    serializer_class = PersPronounSerializer
    # lookup_field = 'slug' or whatever
