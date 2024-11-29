from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email', }
        ))

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Name', }
        ))

    message = forms.CharField(
        label='Your Message',
        widget=forms.Textarea(
            attrs={'placeholder': 'Your Message', }
        ))
