from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from .models import Profile, User

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = ""
        try:
            profile = Profile.objects.get(user=request.user.id)
            path = "/view/Dashboard"
        except Profile.DoesNotExist:
            path = "/profile/setup"

        return path.format(username=request.user.username)
