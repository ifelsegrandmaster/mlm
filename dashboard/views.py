from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView;
from django.urls import reverse
from dashboard.models import Payment
from users.models import User, Profile
from django.http import JsonResponse
from .forms import *
from django.forms import Form
from django.core import serializers
from django_countries import countries
from django.http import HttpResponseRedirect
from .models import SocialLinks, EmailID
from .forms import SocialLinksForm
from django.core.mail import send_mail



# Create your views here.
class DashboardView(TemplateView):
    template_name = "dashboard/index.html"


def home(request, action):
    admin = ['Dashboard', 'Manage', 'Profile', 'Payments']
    ordinary = ['Dashboard', 'Profile']
    actions = []

    if request.user:
        if request.user.is_staff:
            actions = admin
        else:
            actions = ordinary

    context = {
        'actions': actions
    }

    if action == 'Manage' and request.user.is_staff:
        # List the users in the database
        users = Profile.objects.order_by('-level')
        context['users'] = users
        context['countries'] = dict(countries)
        context['active'] = 'Manage'
    if action == 'Profile':
        # Show the user profile and the matrix
        try:
            profile = Profile.objects.get(user=request.user.id)
            context['user_profile'] = profile
            context['children'] = profile.child_of.all()
            context['grandchildren'] = profile.grand_child_of.all()
            context['id'] = request.user.profile.pk
            context['active'] = 'Profile'
        except Profile.DoesNotExist:
            context['message'] = '''You are receiving this message because your profile is no longer active
            .It has been deactivated by the admin. This is because you have been paid. You can now open another 
            account and do the same process. If not paid kindly contact us in the details provided at our homepage'''
            context['title'] = 'Account inactive'

        
        

    if action == 'Payments':
        # Show a list of users to pay
        payments = Payment.objects.filter(completed=False)
        if payments.count() == 0:
            payments = Payment.objects.filter(completed=True)
            context['reversed'] = 'yeah'
        context['payments'] = payments
        context['id'] = request.user.id
        context['active'] = 'Payments'
        

    if action == 'Withdraw' and request.user.profile.can_withdraw:
        # Bring in the user form
        context['active'] = 'Withdraw'

        if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                bank = form.cleaned_data['bank']
                account = form.cleaned_data['account']
                profile = Profile.objects.get(pk=request.user.id)
                payment = Payment(profile=profile, bank=bank, account=account)
                payment.save()
                profile.can_withdraw = False
                profile.save()
                context[
                    'message'] = 'Thanks for submitting you banking details. Your money will be deposited in your bank account. After you receive your money your account will be deactivated'
                context['title'] = 'Thank you'
                context['success'] = 'Yes'
        else:
            form = PaymentForm()
            print(form)
            context['payment_form'] = form
    else:
        if action == 'Withdraw':
            context['message'] = 'This page is disabled, you cannot withdraw now'
            context['title'] = 'Page not working'

    if action == 'Dashboard' and request.user.is_staff:
       payments = Payment.objects.all()
       profiles = Profile.objects.all()
       profiles_count = profiles.count()
       payments_count = payments.count()
       active_count = Profile.objects.filter(is_active=True).count()
       level1_count = Profile.objects.filter(level=1).count()
       level2_count = Profile.objects.filter(level=2).count()
       pending_withdrawals_count = Payment.objects.filter(completed=False).count()
       completed_withdrawals_count = Payment.objects.filter(completed=True).count()

       context['payments_count'] = payments_count
       context['users_count'] = profiles_count
       context['active_count'] = active_count
       context['not_active_count'] = profiles_count - active_count
       context['withdrawals_count'] = payments_count
       context['level1_count'] = level1_count
       context['level2_count'] = level2_count
       context['pending_withdrawals_count'] = pending_withdrawals_count
       context['completed_withdrawals_count'] = completed_withdrawals_count
       
       context['dashboard'] = 'admin'
       context['id'] = request.user.id
       context['active'] = 'Dashboard'
    
    elif action == 'Dashboard' and not request.user.is_staff:
        try:
            profile = request.user.profile
            count = profile.child_of.all().count() + profile.grand_child_of.all().count()
            context['dashboard'] = 'ordinary'
            context['count'] = count
            context['cash'] = profile.balance
            context['level'] = profile.level
            context['profile'] = profile
            context['id'] = request.user.id
            context['active'] = 'Dashboard'
        except Profile.DoesNotExist:
            return HttpResponseRedirect(reverse('setup'))
    
    if action == 'Compansation':
        context['header'] = 'Compansation plan'
        context['title1'] = 'First level'
        context['body1'] = {
            'text1': 'Join with 250',
            'text2': 'Recruit two to directly come under you',
            'text3': 'Level 1 completed'
        }
        context['title2'] = 'Second level'
        context['body2'] = {
            'text1': 'Teach 2 to get their 2. Level 2 completed',
            'text2': 'Withdraw 1000',
            'text3': 'Start another account'
        }
    if action == 'Settings' and request.user.is_staff:
        try:
            link = SocialLinks.objects.get(pk=1)
            form = SocialLinksForm(instance=link)
        except SocialLinks.DoesNotExist:
            form = SocialLinksForm()
        try:
            links = SocialLinks.objects.get(pk=1)
            if request.method == 'POST':
                form = SocialLinksForm(request.POST, instance=links)
                social = form.save()
        except SocialLinks.DoesNotExist:
            form = SocialLinksForm()
            if request.method == 'POST':
                form = SocialLinksForm(request.POST)
                social = form.save()
                print(social)
        admins = User.objects.filter(is_staff=True)
        context['socialform'] = form
        context['admins'] = admins
        

    
    return render(request, 'dashboard/index.html', context)


def fire(request, id):
    user = User.objects.get(id=id)
    if request.user.is_superuser:
        user.is_staff = False
        user.save()
        return JsonResponse({
            "message": "User fired successfully",
            "code": 1
        })
    else:
        return JsonResponse({
            "message": "Sorry you do not have enough privilledges",
            "code": -1
        })
    return JsonResponse({"message": "Nothing done", code: 0})

def details(request, action, id):
    admin = ['Dashboard', 'Manage', 'Profile', 'Payments']
    adminicons = ['fa-home', 'fa-users', 'fa-user', 'fa-money-bill-alt']
    ordinary = ['Dashboard', 'Profile']
    ordinaryicons = ['fa-home', 'fa-user']

    actions = []
    icons = []

    if request.user:
        if request.user.is_staff:
            actions = admin
            icons = adminicons
        else:
            actions = ordinary
            icons = ordinaryicons
    context = {
        'actions': actions,
        'icons': icons
    }

    profile = Profile.objects.get(user=id)
    context['user_profile'] = profile
    context['children'] = profile.child_of.all()
    context['grandchildren'] = profile.grand_child_of.all()
    context['id'] = id

    return render(request, 'dashboard/index.html', context)


def activate(request, id):
    message = ''
    code = -1
    if request.method == 'GET':
        user = Profile.objects.get(pk=id)
        if user.is_active:
            user.is_active = False
            message = 'User has been deactivated'
            code = 0
        else:
            user.is_active = True
            user.is_new = False
            message = 'User has been activated'
            code = 1
        
        user.save()
    return JsonResponse({'message': message, 'code': code, 'id': id})


def get_user_data(request, id):
    message = ''
    code = -1
    count = 0
    level = 0
    cash = 0
    if request.method =='GET':
        profile = Profile.objects.get(pk=id)
        count = profile.child_of.all().count() + profile.grand_child_of.all().count()
        level = profile.level
        cash = profile.balance
        code = 1
    return JsonResponse({'message': message,
    'code':code,
    'count': count, 
    'id': id,
    'level': level,
    'cash': cash
    })
    


from .forms import SendEmailForm
from django.core.mail import send_mail
def index(request):
    context = {}
    try:
        social = SocialLinks.objects.get(id=1)
        context['social'] = social
    except SocialLinks.DoesNotExist:
        pass

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home", args=['Dashboard']))
    if request.method=='POST':
        send_mail_form = SendEmailForm(request.POST)
        if send_mail_form.is_valid():
            address = send_mail_form.cleaned_data['email']
            message = send_mail_form.cleaned_data['body']
            
            context['message'] = 'Thank you your message has been successfully sent.'
        

    return render(request, "dashboard/home.html", context)


def fetch(request, id):
    profile = Profile.objects.get(pk=id);
    children = []
    grandchildren = []

    for child in profile.child_of.all():
        cdata = {}
        cdata['fname'] = child.first_name
        cdata['lname'] = child.last_name
        cdata['phone'] = child.phone
        cdata['children'] = []
        for grandchild in child.child_of.all():
            gcdata = {}
            gcdata['fname'] = grandchild.first_name
            gcdata['lname'] = grandchild.last_name
            gcdata['phone'] = grandchild.phone
            cdata['children'].append(gcdata)
        children.append(cdata)

    data = {
        'children': children,
        'parent': {
            'fname': profile.first_name,
            'lname': profile.last_name,
            'phone': profile.phone
        }
    }

    return JsonResponse(data)

def search(request,category,keyword):
    if request.method == 'GET':
        print("Something happened at least") 
        keyword = keyword
        if category == 'name':
             profiles = Profile.objects.filter(first_name__icontains=keyword)
             data = serializers.serialize("json", profiles)
             print(data)
             return JsonResponse({"data": data})
        if category == 'country':
            profiles = Profile.objects.filter(country=keyword)
            data = serializers.serialize("json", profiles)
            print(data)
            return JsonResponse({"data": data})
        if category == 'activity':
            value = int(keyword)
            if value == 0:
                profiles = Profile.objects.filter(is_active=False)
                data = serializers.serialize("json", profiles)
                print(data)
                return JsonResponse({"data": data})
            if value == 1:
                profiles = Profile.objects.filter(is_active=True)
                data = serializers.serialize("json", profiles)
                print(data)
                return JsonResponse({"data": data})
            else:
                profiles = Profile.objects.all()
                data = serializers.serialize("json", profiles)
                print(data)
                return JsonResponse({"data": data})



       
    return JsonResponse({
        "message": "Nada"
    })


def get_payments(request,keyword):
    if keyword == 'completed':
        payments = Payment.objects.filter(completed=True)
        data = []
        for payment in payments:
            pdata = {}
            pdata['bank'] = payment.bank
            pdata['accountNumber'] = payment.account
            pdata['firstname'] = payment.profile.first_name
            pdata['surname']  = payment.profile.last_name
            pdata['balance'] = payment.profile.balance
            pdata['id'] = payment.profile.pk
            data.append(pdata)
        return JsonResponse({"data": data})
    if keyword == 'pending':
        payments = Payment.objects.filter(completed=False)
        data = []
        for payment in payments:
            pdata = {}
            pdata['bank'] = payment.bank
            pdata['accountNumber'] = payment.account
            pdata['firstname'] = payment.profile.first_name
            pdata['surname'] = payment.profile.last_name
            pdata['balance'] = payment.profile.balance
            pdata['id'] = payment.profile.pk
            pdata['pk'] = payment.pk
            data.append(pdata)
        return JsonResponse({"data": data})
    return JsonResponse({"data": "Nada"})

def pay(request, pk):
    payment = Payment.objects.get(id=pk)
    payment.completed = True
    payment.save()
    user = payment.profile.user
    profile = payment.profile
    profile.is_active = False
    profile.save()
    user.is_active = False
    user.save()
    return JsonResponse({"message": "Payment was made"})

def register(request):
    user = request.user
    print(user)
    parent = user.profile.is_child_of
    grandparent = user.profile.is_grand_child_of
            
    if parent.child_of.all().count() == 2:
            parent.level = 1
            parent.save()
    if grandparent.grand_child_of.all().count() == 4:
            grandparent.level = 2
            grandparent.can_withdraw = True
            grandparent.save()
    
    profile = Profile.objects.get(user=user)
    profile.is_new = False
    profile.save()
    return JsonResponse({"message":"OK"})

def get_dashboard_data(request):
    active_count = Profile.objects.filter(is_active=True).count()
    not_active_count = Profile.objects.filter(is_active=False).count()
    level1_count = Profile.objects.filter(level=1).count()
    level2_count = Profile.objects.filter(level=2).count()
    users_count = Profile.objects.count()
    payments_count = Payment.objects.count()
    pending_payments = Payment.objects.filter(completed=False).count()
    completed_payments = Payment.objects.filter(completed=True).count()
    data = {
            'active': active_count,
            'not_active':not_active_count,
            'level1': level1_count,
            'level2': level2_count,
            'users': users_count,
            'completed': completed_payments,
            'payments': payments_count,
            'pending': pending_payments
    }

    return JsonResponse(data)


def tandcs(request):
    context = {}
    return render(request, 'tandcs.html', context)

from decimal import *

def delete_user(request,id):
    if request.method == "GET":    
        if request.user.is_authenticated and request.user.is_superuser:
            try:
                profile = Profile.objects.get(pk=id)
                parent = profile.is_child_of
                grandparent = profile.is_grand_child_of
                parent.balance = Decimal(parent.balance) - Decimal(166.66666666666)
                grandparent.balance = Decimal(grandparent.balance) - Decimal(166.66666666666)
                parent.save()
                grandparent.save()
                if profile.child_of.all().count() > 0:
                    return JsonResponse({"message": "Cannot delete user", "code": 0})
                user = User.objects.get(profile=profile)
                user.delete()
                if parent.child_of.all().count() < 2:
                    parent.level = 0
                    parent.save()
                if grandparent.grand_child_of.all().count() < 4:
                    grandparent.level = 1
                    grandparent.save()
                
                return JsonResponse({"message": "Successfully deleted user", "code": 1})
            except Profile.DoesNotExist:
                return JsonResponse({"messaage": "User does not exist in our system", "code": -1})
def get_users(request):
    if request.method == 'GET':
        users = User.objects.filter(is_staff=False)
        data = serializers.serialize("json", users)
        return JsonResponse({"users": data})
    return JsonResponse({"message": "Empty"})

def make_admin(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'GET':
            try:
                user = User.objects.get(id=id)
                user.is_staff = True
                user.save()
                return JsonResponse({"message": "Operation successful", "code": 1})
            except User.DoesNotExist:
                return JsonResponse({"message": "User does not exist", "code":-1})
    else:
        return JsonResponse({"message": "Not enough privilleges", "code": -1})
    return JsonResponse({"message": "Nothing done", "code": 0})

def add_email_address(request):
    if request.method == "POST":
        email_id = request.POST.get('email', '')
        #search if the email already exists
        try:
            email_db_entry = EmailID.objects.get(email_id=email_id)
            return render(request, "dashboard/subscription.html", 
            {"message": "You are already subscribed to our newsletters."}) 
        except EmailID.DoesNotExist:
            email_db_entry = EmailID(email_id=email_id)
            email_db_entry.save()
            return render(request, "dashboard/subscription.html", 
            {"message": "Thanks for subscribing to our newsletters."})
             
    return redirect("/")

#send email to subscribers view
def send_email(request):
    #if the user visiting here is not staff redirect the unauthorized access page
    if  not request.user.is_staff:
        return redirect('/unauthorized')
    
    #Of cause send html content
    send_email_form = SendEmailForm()  
    if request.method == "POST":
        #bind the form with the POSTed data
        send_email_form = SendEmailForm(request.POST)
        if send_email_form.is_valid():
            #get the html content
            html_content = send_email_form.cleaned_data["html_content"]
            #get the subject
            subject = send_email_form.cleaned_data["subject"]
            #email sent from
            email_from = "abantusoft@gmail.com"
            #email to[] load them from the database
            emails = EmailID.objects.all()
            #emails to
            emails_to = []

            for email_id in emails:
                emails_to.append(email_id.email_id)
            #now construct the email
            send_mail(
                subject,
                html_content,
                email_from,
                emails_to,
                fail_silently=False,          
            )
            #return a redirect to the email sent successfully page
            return redirect("/email-sent")
        else:
            #return a form with errors
            return render(request, "dashboard/send_email.html", {"form": send_email_form})
    #return a response with an unbounded form        
    return render(request, "dashboard/send_email.html", {"form": send_email_form})

#unauthorized view
def unauthorized(request):
    return render(request, "dashboard/unauthorized.html", {})
    
#email sent
def email_sent(request):
    return render(request, "dashboard/email_sent.html", {})

