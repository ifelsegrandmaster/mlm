from django.db import models
from users.models import Profile
from uuid import *
# Create your models here.

class Payment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="payment")
    bank = models.CharField(max_length=100)
    account = models.CharField(max_length=12)
    completed = models.BooleanField(default=False)

class Group(models.Model):
    name = models.CharField(max_length=50)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)

class SocialLinks(models.Model):
    facebook = models.URLField(max_length=200)
    twitter = models.URLField(max_length=200)
    whatsapp = models.URLField(max_length=200)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50)

class EmailID(models.Model):
    email_id = models.EmailField()

    def __str__(self):
        return self.email_id

    
