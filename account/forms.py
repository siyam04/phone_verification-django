from django import forms

class VerifiedPhoneForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'phone_number'}))

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'exampleInputPhone',
                                                                 'placeholder': 'Enter Your Mobile Number'}))

class CheckOtpForm(forms.Form):
    otp_code = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'exampleInputPhone',
                                                                'placeholder': 'Activation Code'}))

class GetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'exampleInputPhone',
                                                                 'placeholder': 'Choose Password'}))
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'exampleInputPhone',
                                                                    'placeholder': 'Re-Password'}))

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'exampleInputPhone',
                                                                 'placeholder': 'Enter Your Mobile Number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'exampleInputPhone',
                                                                 'placeholder': 'Enter Password'}))
