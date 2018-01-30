from rest_framework import serializers
from .models import ExNNS, ExAAS, ExLNS, ExIIV, ExKKV


class ExNNSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExNNS
        fields = ('id', 'german')


class ExAASSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExAAS
        fields = ('id', 'german')


class ExLNSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExLNS
        fields = ('id', 'german')


class ExIIVSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExIIV
        fields = ('id', 'german')


class ExKKVSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExKKV
        fields = ('id', 'german')
