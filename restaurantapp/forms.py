from django import forms
#from django.contrib.auth.forms import
from django.contrib.auth.models import User
from restaurantapp.models import Customer

#===============Profile form Start========================#
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','locality','city','mobile','state','zipcode']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        }
#===============Profile form End========================#