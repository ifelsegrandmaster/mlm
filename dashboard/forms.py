from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm
from django import forms
from .models import Payment, SocialLinks

class MLMLoginForm(LoginForm):

    def login(self, *args, **kwargs):
        #Add more processing
        return super(MLMLoginForm, self).login(*args, **kwargs)

class MLMSignupForm(SignupForm):

    def save(self, request):
        #Ensure you call the parent classes save
        user = super(MLMSignupForm, self).save(request)
        #Add extra processing

        #Get the code used to sign up and give credit to the owner
        return user

class PaymentForm(forms.Form):

    bank = forms.CharField(label='Your bank', max_length=100)
    account = forms.CharField(label='Your account number', max_length=12)

class SearchForm(forms.Form):
    search = forms.CharField(label='Search',required=True)

class SendEmailForm(forms.Form):
    email = forms.EmailField(max_length=200,required=True)
    body = forms.CharField(max_length=20000)

class SocialLinksForm(forms.ModelForm):

    
    class Meta:
         fields = ('facebook', 'twitter', 'whatsapp', 'email', 'phone')
         model = SocialLinks
class SendEmailForm(forms.Form):
    subject = forms.CharField(max_length=100)
    html_content = forms.CharField(widget=forms.Textarea)


