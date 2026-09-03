from django import forms
from django.forms import ModelForm
from .models import room
from .models import update,cash_expenditure, message, Msg,MpesaTransaction
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError
from .models import WhatsAppContact
from .models import OpeningBalance


class OpeningBalanceForm(forms.ModelForm):
    class Meta:
        model = OpeningBalance
        fields = ['amount', 'balance_date', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'balance_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }



class RoomForm(ModelForm):
    class Meta:
        model=room
        fields='__all__'
        exclude = ['host']

class MsgForm(ModelForm):
    class Meta:
        model=Msg
        fields='__all__'
        exclude = ['host']

class MessageForm(ModelForm):
    class Meta:
        model=message
        fields='__all__'
        exclude = ['host']        


class cash_expenditureForm(ModelForm):

    class Meta:
        model = cash_expenditure
        fields = "__all__"
        exclude = ["host"]

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
        }
  

class UpdateForm(ModelForm):
    class Meta:
        model=update
        fields = ['user_name','transaction',  "choose", "choice"]


         

class CustomUserCreationForm(UserCreationForm): 
    username = forms.CharField(required=True)  
    email = forms.EmailField(required=True)  
   

    class Meta:  
        model = User  
        fields = ('username', 'email',  'password1', 'password2')

    def clean_username(self):  
        username = self.cleaned_data.get('username')  
        if User.objects.filter(username=username).exists():  
            raise ValidationError("This username is already taken.")  
        return username    
    

class WhatsAppMessageForm(forms.Form):
    contacts = forms.ModelMultipleChoiceField(
        queryset=WhatsAppContact.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    message = forms.CharField(widget=forms.Textarea, required=True)   

class MpesaForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)
    amount = forms.IntegerField()    

class BulkMessageForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Type your message here...",
            "rows": 4
        })
    )

    send_to_all = forms.BooleanField(required=False)


class MpesaTransactionForm(forms.ModelForm):

    class Meta:
        model = MpesaTransaction

        fields = [
            'user',
            'profile',
            'full_name',
            'phone_number',
            'amount',
            'checkout_request_id',
            'merchant_request_id',
            'mpesa_receipt_number',
            'transaction_date',
            'status',
            'result_code',
            'result_desc',
        ]

        widgets = {

            'user': forms.Select(attrs={
                'class': 'form-control'
            }),

            'profile': forms.Select(attrs={
                'class': 'form-control'
            }),

            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),

            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount'
            }),

            'checkout_request_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Checkout Request ID'
            }),

            'merchant_request_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Merchant Request ID'
            }),

            'mpesa_receipt_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mpesa Receipt Number'
            }),

            'transaction_date': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Transaction Date'
            }),

            'status': forms.Select(attrs={
                'class': 'form-control'
            }),

            'result_code': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Result Code'
            }),

            'result_desc': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Result Description'
            }),
        }
        