from django import forms
from django.core.validators import RegexValidator

from Cosmetic_studio.orders.models import Order, ShippingAddress


class CheckoutForm(forms.ModelForm):
    MAX_POSTAL_CODE_LENGTH = 10

    name = forms.CharField(
        max_length=ShippingAddress.MAX_NAME_LENGTH,
    )

    phone_number = forms.CharField(
        max_length=ShippingAddress.MAX_PHONE_NUMBER_LENGTH,
        validators=[RegexValidator(
            regex=r"^0\d{9}$",
            message="Please, enter a valid phone number in the format 0888123456"
        )]
    )

    email = forms.EmailField()

    address = forms.CharField(
        widget=forms.Textarea,
    )

    city = forms.CharField(
        max_length=ShippingAddress.MAX_CITY_LENGTH,
    )

    postal_code = forms.CharField(
        max_length=MAX_POSTAL_CODE_LENGTH,
    )

    payment_method = forms.ChoiceField(
        choices=ShippingAddress.PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        initial='pay_on_delivery'
    )

    class Meta:
        model = Order
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self._prepopulate_fields()

    def _prepopulate_fields(self):
        last_order = ShippingAddress.objects.filter(customer=self.user).order_by('-created_at').first()
        if last_order:
            self.fields['name'].initial = last_order.name
            self.fields['phone_number'].initial = last_order.phone_number
            self.fields['email'].initial = last_order.email
            self.fields['address'].initial = last_order.address
            self.fields['city'].initial = last_order.city
            self.fields['postal_code'].initial = last_order.postal_code
        else:
            self.fields['name'].initial = self.user.user_name
            self.fields['phone_number'].initial = self.user.profile.phone_number
            self.fields['email'].initial = self.user.email

    def clean(self):
        cleaned_data = super().clean()
        cart_items = self.user.cart.items.all()
        cleaned_data['total_price'] = sum(item.product.price * item.quantity for item in cart_items)
        cleaned_data['status'] = 'Pending'
        return cleaned_data

    def save(self, commit=True):
        order = super().save(commit=False)
        order.customer = self.user
        order.total_price = self.cleaned_data['total_price']
        order.status = self.cleaned_data['status']

        if commit:
            order.save()

            ShippingAddress.objects.create(
                name=self.cleaned_data['name'],
                phone_number=self.cleaned_data['phone_number'],
                email=self.cleaned_data['email'],
                customer=self.user,
                order=order,
                address=self.cleaned_data['address'],
                city=self.cleaned_data['city'],
                postal_code=self.cleaned_data['postal_code'],
            )

            return order
