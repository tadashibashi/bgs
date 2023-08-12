from django import forms

class CheckboxField(forms.BooleanField):
    widget=forms.CheckboxInput(attrs={"class": "form-check-input ms-2"})
    required=False
