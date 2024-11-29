from django import forms

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        min_value=0.01,  # Ensures the value is positive
        label="Deposit Amount",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter deposit amount'})
    )

    def clean_amount(self):
        min_deposit_amount = 100  # Minimum required deposit amount
        amount = self.cleaned_data.get('amount')

        if amount is None:
            raise forms.ValidationError('This field is required.')

        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount
