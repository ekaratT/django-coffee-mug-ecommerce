from django.forms import ModelForm
from .models import User, UserProfile
from django import forms
from . validators import image_validator
from django.contrib.auth.forms import PasswordChangeForm
from coffee_mug.models import Categories, Products


class CreateuserForm(ModelForm):
    # Extrafield
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(CreateuserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'password':
                self.fields[name].widget.attrs['placeholder'] = 'Password'
            elif name == 'confirm_password':
                self.fields[name].widget.attrs['placeholder'] = 'Confirm password'
            else:
                self.fields[name].widget.attrs['placeholder'] = field.label


    def clean(self):
        cleaned_data = super(CreateuserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password does not match!')


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'address', 'country', 'state', 'city', 'pin_code']
        exclude = ['user', 'created_date', 'modified_date']

    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_new_password = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super(CustomPasswordChangeForm, self).clean()
        old_password = cleaned_data.get('old-password')
        new_password = cleaned_data.get('new-password')
        confirm_password = cleaned_data.get('confirm-password')

        if new_password != confirm_password:
            raise forms.ValidationError('Password does not match!')


class CategoryForm(ModelForm):
    category_picture = forms.FileField(widget=forms.FileInput(), validators=[image_validator])
    class Meta:
        model = Categories
        fields = '__all__'
        exclude = ['created_date', 'modified_date']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            f'<label class="form-input-label">{field.label}</label>'
            field.widget.attrs['class'] = 'input'


class ProductForm(ModelForm):
    product_picture = forms.FileField(widget=forms.FileInput(), validators=[image_validator])
    

    class Meta:
        model = Products
        fields = '__all__'
        exclude = ['created_date', 'modified_date']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input'


