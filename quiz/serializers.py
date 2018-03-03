from rest_framework import serializers
from .models import ExNNS, ExAAS, ExLNS, ExIIV, ExKKV, ExPPV, ExFFV

import random


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


class GermanPronounField(serializers.RelatedField):
    def to_representation(self, value):
        pronouns = value.options['1'].split(',')
        pronoun = random.choice(pronouns)
        return value.german.replace('OPT1', pronoun)


class ExKKVSerializer(serializers.ModelSerializer):
    german = GermanPronounField(source='*', read_only=True)

    class Meta:
        model = ExKKV
        fields = ('id', 'german')


class ExPPVSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExPPV
        fields = ('id', 'german')


class ExFFVSerializer(serializers.ModelSerializer):
    german = GermanPronounField(source='*', read_only=True)

    class Meta:
        model = ExFFV
        fields = ('id', 'german')
