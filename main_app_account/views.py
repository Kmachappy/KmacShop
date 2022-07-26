from email import message
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .token import account_activation_token
from .models import UserBase

@login_required
def dashboard(request):
    return render(request,'account/user/dashboard.html')

# no email activation required
def account_register(request):    
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('main_app_account:dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': form})

# def account_register(request):    
#     if request.user.is_authenticated:
#         return redirect('/')
    
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.email = form.cleaned_data['email']
#             user.set_password(form.cleaned_data['password'])
#             user.is_active = False
#             user.save()
#             # setup email
#             current_site = get_current_site(request)
#             subject = 'Activate your Account'
#             message = render_to_string('account/registration/account_activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
            
#             user.email_user(subject=subject, message=message)
#             return HttpResponse('registered succesfully and activation sent')
#     else:
#         form = RegistrationForm()
#     return render(request, 'account/registration/register.html', {'form': form})

def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('main_app_account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')

