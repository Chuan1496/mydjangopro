from django import forms

class ProductForm(forms.Form):
    id = forms.IntegerField(required=False)
    selectedCate = forms.CharField(required=False)
    selectedBrand = forms.CharField(required=False)
    selectedSup = forms.CharField(required=False)
    prodName = forms.CharField(required=False)