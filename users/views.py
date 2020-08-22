from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse
from users.forms import UserProfileForm
from .models import User, Profile


# Create your views here.
class ProfileView(TemplateView):
    template_name = "users/profile.html"


def error(request):
    context = {}

    return render(request, 'users/error.html', context)


def profile(request):
    user = User.objects.get(pk=request.user.id)

    user_profile = Profile.objects.get(user=request.user.id)

    children = user_profile.child_of.all()
    grandchildren = user_profile.grand_child_of.all()

    context = {
        'user': user,
        'user_profile': user_profile,
        'children': children,
        'grandchildren': grandchildren

    }

    return render(request, 'users/profile.html', context)


from django.views.generic import FormView


class NewUserProfileView(FormView):
    template_name = "users/setup.html"
    form_class = UserProfileForm

    def form_valid(self, form):
        form.save(self.request.user)
        return super(NewUserProfileView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse("home", args=['Dashboard'])

def setup(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        form.save(request.user)
    context = {
        'form': form
    }
    return render(request, 'users/setup.html', context)
