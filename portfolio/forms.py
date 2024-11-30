

# # portfolio/forms.py
# from django import forms
# from .models import Stock

# class StockForm(forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = ['ticker', 'purchase_price', 'quantity']

# portfolio/forms.py
from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'ticker', 'purchase_price', 'quantity']  # Ensure 'name' is included

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("This field cannot be empty.")
        return name
