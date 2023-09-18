from django.forms import ModelForm
from . models import Order
from django import forms

class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'state', 'city', 'country', 'pin_code']

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            self.fields[name].widget.attrs['required'] = 'true'
            # self.fields[name].widget.attrs['name'] = name
            field.widget.attrs['class'] = 'input'


class UnauthenticatedOrderFrom(forms.Form):
    session_key = forms.CharField(max_length=50)
    payment_method = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=100, required=True)
    phone = forms.CharField(max_length=10, required=True)
    address = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=50, required=True)
    city = forms.CharField(max_length=50, required=True)
    country = forms.CharField(max_length=50, required=True)
    pin_code = forms.CharField(max_length=50, required=True)
    is_paid = forms.BooleanField(widget=forms.HiddenInput(), initial=False)

    class Meta:
        exclude = ['user_session', 'payment_method', 'is_paid']

    def __init__(self, *args, **kwargs):
        super(UnauthenticatedOrderFrom, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'is_paid':
                self.fields[name].label= ''
                self.fields[name].widget.attrs['class'] = 'hide-field'
