from django.forms import ModelForm
# from django.forms.widgets import RadioSelect  # noqa: F401
from django import forms

from .models import Noun, Verb


class WordForm(forms.Form):
    czech = forms.CharField(
        label='Tschechisches Wort',
    )
    # chapter = forms.IntegerField(
    #     required=False,
    #     widget=RadioSelect,
    #     choices=CHAPTER_CHOICES,
    #     )


class NounForm(ModelForm):
    class Meta:
        model = Noun
        fields = '__all__'   # ['czech', 'chapter']
        # exclude = ['artikel']
        # widgets = {
        #     'gender_cz': RadioSelect(attrs={
        #         'choices': GENDER_CHOICES,
        #     }),
        #     'gender_de': RadioSelect(attrs={
        #         'choices': GENDER_CHOICES,
        #     }),
        # }


class VerbForm(ModelForm):
    class Meta:
        model = Verb
        fields = '__all__'
