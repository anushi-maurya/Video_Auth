from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    # Password fields (hidden input boxes)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        # Use Django's User model
        model = User
        # Fields to show in the form
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean_password(self):
        """Check if the password is valid"""
        password = self.cleaned_data.get('password')

        # Simple check for length
        if password and len(password) < 8:
            raise forms.ValidationError('Enter a valid password.')
        
        return password

    def clean_confirm_password(self):
        """Check if password and confirm_password match"""
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm_password')

        # Only check if both fields have values
        if password and confirm:
            if password != confirm:
                raise forms.ValidationError('Passwords do not match.')
        
        return confirm
