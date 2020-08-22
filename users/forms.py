# users/forms.py
import random
import string

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile
from decimal import *
from django.forms.forms import NON_FIELD_ERRORS
from channels.layers import get_channel_layer


def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


""""
This is responsible for saving User profile only

"""


class UserProfileForm(forms.ModelForm):
    code = forms.CharField(label='Referal code')

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'address', 'phone', 'country')

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Firstname'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Lastname'}),
            'address': forms.TextInput(attrs={'placeholder': 'Home address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'code': forms.TextInput(attrs={'placeholder': 'Referal code'})
        }

    def save(self, user=None):
        try:
            profile = Profile.objects.get(user=user)
            return profile
        except Profile.DoesNotExist:
            user_profile = super(UserProfileForm, self).save(commit=False)
            if user:
                user_profile.user = user
                code = self.cleaned_data['code']
                print(code)
                # Add this user to the matrix

                try:
                    parent = Profile.objects.get(code=code)
                except Profile.DoesNotExist:
                    self.clean()
                grandparent = parent.is_child_of

                user_profile.is_child_of = parent
                user_profile.is_grand_child_of = grandparent
                # Raise the level
                if parent.child_of.all().count() == 2:
                    parent.level = 1
                    parent.save()
                if grandparent.grand_child_of.all().count() == 4:
                    grandparent.level = 2
                    grandparent.can_withdraw = True
                    grandparent.save()

            # Get back to this later
            usercode = code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            user_profile.code = usercode
            user_profile.save()

            grandparent.balance = Decimal(grandparent.balance) + Decimal(166.66666666666)
            grandparent.save()
            parent.balance = Decimal(parent.balance) + Decimal(166.66666666666)
            parent.save()
        print("Profile saved")
        return user_profile
    

    # Validate the code entered by the new user
    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        try:
            parent = Profile.objects.get(code=code)
            if parent.child_of.all().count() == 2:
                raise forms.ValidationError(
                    "You can no longer join with this code, only a maximum of two people allowed",
                    'join not allowed'
                )
        except Profile.DoesNotExist:
            raise forms.ValidationError(
                "The code you used is invalid",
                'code not available'
            )
