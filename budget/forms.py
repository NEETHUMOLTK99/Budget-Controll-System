from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Expense
from django.contrib.admin.widgets import AdminDateWidget


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2"]



class ExpensCreateForm(ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model=Expense
        fields="__all__"
        widgets={
            "notes":forms.TextInput(attrs={'class':'form-control'}),
            "amount": forms.TextInput(attrs={'class': 'form-control'}),
            "user": forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}) #user cannot edit
        }
#overriding uses
    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")
        if amount < 50:
            msg = "invalid amount"
            self.add_error("amount", msg)


class DateSearchForm(forms.Form):
    date=forms.DateField(widget=forms.SelectDateWidget())


class RevieExpensForm(forms.Form):
    from_date=forms.DateField(widget=forms.SelectDateWidget)
    to_date=forms.DateField(widget=forms.SelectDateWidget)