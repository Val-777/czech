# from django.forms.widgets import RadioSelect  # noqa: F401
from django import forms


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


class ExPPVForm(forms.Form):
    czech = forms.CharField(
        label='',
        help_text='Tschechische Übersetzung hier eingeben, in Klammern steht das Geschlecht des Subjekts',
    )
