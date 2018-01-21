from rest_framework import serializers
from .models import ExNNS, ExAAS


class ExNNSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExNNS
        fields = ('id', 'german')


class ExAASSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExAAS
        fields = ('id', 'german')
