from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from datetime import datetime
# Create your models here.



class User(AbstractUser):
    pass



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=500, default='')
    country = CountryField(blank_label='(select country)')
    phone = models.CharField(max_length=12)
    level = models.IntegerField(default=0)
    is_child_of = models.ForeignKey("self",on_delete=models.CASCADE, related_name='child_of')
    is_grand_child_of = models.ForeignKey("self", on_delete=models.CASCADE, related_name='grand_child_of')
    is_active = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    code = models.CharField(max_length=6)
    can_withdraw = models.BooleanField(default=False)
    balance = models.DecimalField(default=0, max_digits=20, decimal_places=12)
    date_joined = models.DateField(default=datetime.now)
    

    def __str__(self):
        return self.first_name + " " + self.last_name



    #more details




