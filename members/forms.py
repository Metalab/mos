import django.forms as forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm

from .models import ContactInfo


class UserNameForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UserInternListForm(ModelForm):
    class Meta:
        model = ContactInfo
        fields = ('on_intern_list', 'intern_list_email')


class UserInternMatrixForm(ModelForm):
    class Meta:
        model = ContactInfo
        fields = ('in_intern_matrix_room', 'matrix_handle')


class UserEmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', )


class UserAdressForm(ModelForm):
    class Meta:
        model = ContactInfo
        fields = ('street', 'city', 'postcode', 'country')


class UserImageForm(ModelForm):
    class Meta:
        model = ContactInfo
        fields = ('image', )
