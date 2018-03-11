from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254,
                            required=True,
                            label='Emailadresse:',
                            widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        passtext = """<ul>
        <li>Ihr Passwort kann Ihren anderen persönlichen Informationen nicht zu ähnlich sein.</li>
        <li>Ihr Passwort muss mindestens 8 Buchstaben enthalten.</li>
        <li>Ihr Passwort kann kein allgemein oft benutztes Passwort sein.</li>
        <li>Ihr Passwort kann nicht nur aus Zahlen bestehen.</li>
        </ul>"""

        self.fields['username'].label = 'Benutzername:'
        self.fields['username'].help_text = '150 Zeichen oder weniger. Buchstaben, Ziffern und @/./+/-/_ erlaubt.'
        self.fields['password1'].label = 'Passwort:'
        self.fields['password1'].help_text = passtext
        self.fields['password2'].label = 'Passwort bestätigen:'
        self.fields['password2'].help_text = ''
