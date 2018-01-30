from django.forms import ModelForm
from django.forms.widgets import RadioSelect  # noqa: F401
from django import forms

from .models import Noun, Verb

# MASCULINE = 'M'
# FEMININE = 'F'
# NEUTER = 'N'
# GENDER_CHOICES = (
#     (MASCULINE, 'Masculine'),
#     (FEMININE, 'Feminine'),
#     (NEUTER, 'Neuter'),
# )


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


class ExNNSForm(forms.Form):
    czech = forms.CharField(
        label='',
        help_text='Tschechische Übersetzung hier eingeben',
    )


class ExAASForm(forms.Form):
    czech = forms.CharField(
        label='Vidím ...',
        help_text='Tschechische Übersetzung hier eingeben',
    )


class ExLNSForm(forms.Form):
    czech = forms.CharField(
        label='Mluvím o ...',
        help_text='Tschechische Übersetzung hier eingeben',
    )


class ExIIVForm(forms.Form):
    czech = forms.CharField(
        label='',
        help_text='Tschechische Übersetzung hier eingeben',
    )


class ExKKVForm(forms.Form):
    czech = forms.CharField(
        label='',
        help_text='Tschechische Übersetzung hier eingeben',
    )
