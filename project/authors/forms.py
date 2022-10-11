import re

from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError


def add_attr(field, attr_name, attr_new_value):
    existing = field.widget.attrs.get('attr_name', '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_value}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter,'
            'one lowercase letter and one number. the length shoud be'
            'at least 8 characters.'
        ),
            code='Invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['repeat_password'], 'Repeat your password')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_attr(self.fields['username'], 'css', 'a-css-class')

    username = forms.CharField(
        label='Username',
        help_text=('Username must have letters, numbers or one of those @.+-_'
                   'The lenght should be between 4 and 150 characters'),
        min_length=4,
        max_length=150,
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters',

        },
    )
    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        label='First name'
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last name'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password],
        label='Password'
    )

    repeat_password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repeat Password',
        error_messages={
            'required': 'Please, repeat your password'
        }
    )

    email = forms.EmailField(
        label='E-mail',
        error_messages={
            'required': 'E-mail is required'
        },
        help_text='The e-mail must be valid.'
    )

    # passar metadados

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password != repeat_password:
            raise ValidationError({
                'password': 'Password and repeat password must be equal',
                'repeat_password': 'Password and repeat password must be equal'
            })
