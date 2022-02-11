from django import forms 
from .models import *


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"
        exclude=['user']


class BlogPageForm(forms.ModelForm):
    class Meta:
        model = BlogPage
        fields = "__all__"
        exclude=['view_count']

class PasswordForgotForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-contro','placeholder':'Email used in customer account'}))
    def clean_email(self):
        e = self.cleaned_data.get('email')
        if Author.objects.filter(user__email=e).exists():
            pass
        else:
            raise forms.ValidationError('Customer with this account doesnot exists...')
        return e