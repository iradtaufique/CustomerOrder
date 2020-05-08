from django.contrib.auth.forms import UserCreationForm
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import *


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'



class SetNumberForm(forms.Form):
    order_number = forms.IntegerField(min_value=1, label='Number of Order', max_value=10)

    # def __init__(self, *args, **kwargs):
    #     super(SetNumberForm, self).__init__(self, *args, **kwargs)
    #     self.fields['order_number'].required = False


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2'
        ]


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ('user',)


class AddTagsForm(ModelForm):
    class Meta:
        model = Tags
        fields = ['name']



class AddProductForm(ModelForm):
    # tags = forms.CharField(widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Product
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(AddProductForm, self).__init__(*args, **kwargs)
    #     self.fields['tags'].widget = forms.CheckboxSelectMultiple()
