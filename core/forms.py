from django import forms
from core.models import Brand, Category, Product, Supplier

class ProductForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta:
        model=Product
        fields=['description','price','stock','brand','categories','line','supplier','expiration_date','image','state']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return price
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock


class BrandForm(forms.ModelForm):
    class Meta:
        model=Brand
        fields=['description','state']

class SupplierForm(forms.ModelForm):
    class Meta:
        model=Supplier
        fields=['name','ruc','address','phone','state']
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['description','state']