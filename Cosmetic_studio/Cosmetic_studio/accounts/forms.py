from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms

from Cosmetic_studio.accounts.models import Profile

UserModel = get_user_model()


class CreateUserForm(auth_forms.BaseUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields["email"].widget.attrs['placeholder'] = 'info@example.com'
        self.fields["user_name"].widget.attrs['placeholder'] = 'Full Name'
        self.fields["password1"].widget.attrs['placeholder'] = 'Password'
        self.fields["password2"].widget.attrs['placeholder'] = 'Password'

    class Meta:
        model = UserModel
        fields = ['email', 'user_name', 'password1', 'password2']
        labels = {
            'user_name': 'Full Name or Nickname',
        }


class StudioUserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = UserModel
        fields = '__all__'


class StudioUserLoginForm(auth_forms.AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"id": "email", "type": "email", "class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password", "id": "password", }))


class ProfileBaseForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['preferred_name_nickname', 'phone_number', 'profile_picture']
        labels = {
            'preferred_name_nickname': 'Preferred Name or nickname',
            'phone_number': 'Phone Number',
            'profile_picture': 'Profile Picture',
        }


class ProfileEditForm(ProfileBaseForm):
    pass


class UpdateProfileForm(ProfileBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ChangePassword(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = UserModel

# TODO implement reset password
