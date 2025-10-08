from django import forms

class PlaceForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    latitude = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))
    longitude = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}))