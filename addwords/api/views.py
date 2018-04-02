from django.db.models import Q

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)

from rest_framework.permissions import (
    IsAdminUser,
)

from addwords.models import PersPronoun
from .serializers import (
    PersPronounSerializer,
    PersPronounCreateSerializer,
)


class PersPronounCreateAPIView(CreateAPIView):
    queryset = PersPronoun.objects.all()
    serializer_class = PersPronounCreateSerializer
    permission_classes = [IsAdminUser, ]


class PersPronounListAPIView(ListAPIView):
    serializer_class = PersPronounSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = PersPronoun.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(gender__iexact=query) |
                Q(chapter__iexact=query) |
                Q(role__iexact=query)
            ).distinct()
        return queryset_list


class PersPronounUpdateAPIView(RetrieveUpdateAPIView):
    queryset = PersPronoun.objects.all()
    serializer_class = PersPronounSerializer
    permission_classes = [IsAdminUser, ]


class PersPronounDeleteAPIView(DestroyAPIView):
    queryset = PersPronoun.objects.all()
    serializer_class = PersPronounSerializer
    permission_classes = [IsAdminUser, ]


class PersPronounDetailAPIView(RetrieveAPIView):
    queryset = PersPronoun.objects.all()
    serializer_class = PersPronounSerializer
    # lookup_field = 'slug' or whatever
