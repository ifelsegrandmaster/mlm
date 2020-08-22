from django.contrib import admin

# Register your models here.
from .models import Payment, SocialLinks, EmailID
admin.site.register(Payment)
admin.site.register(SocialLinks)
admin.site.register(EmailID)
