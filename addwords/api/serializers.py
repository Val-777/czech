from rest_framework.serializers import ModelSerializer

from addwords.models import PersPronoun


class PersPronounCreateSerializer(ModelSerializer):
    class Meta:
        model = PersPronoun
        fields = [
            'chapter',
            'german',
            'czech',
            'role',
            'gender',
        ]


class PersPronounSerializer(ModelSerializer):
    class Meta:
        model = PersPronoun
        fields = [
            'id',
            'chapter',
            'german',
            'czech',
            'role',
            'gender',
        ]
