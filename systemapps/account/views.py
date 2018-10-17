from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, is_safe_url
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from .forms import *
from area.models import Owner
from area.forms import SendOwnerRequest


# Create your views here.

def LoginSignupView(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        signup_form = SignupForm(data=request.POST)

        if 'login-form-submit' in request.POST:
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                next_url = request.POST.get('next', None)  # Checking the next URL and redirect
                url_is_safe = is_safe_url(url=next_url, allowed_hosts=settings.ALLOWED_HOSTS,
                                          require_https=request.is_secure())
                if next_url and url_is_safe:
                    return redirect(next_url)
                return redirect('home')

        if 'signup-form-submit' in request.POST:
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.is_active = False
                user.save()

                domain = request.get_host()
                mail_subject = 'Активация личного кабинета: ' + domain
                mail_message = render_to_string('mail_accountactivation.html',
                                                {'user': user,
                                                 'domain': domain,
                                                 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                                                 'token': account_activation_token.make_token(user)})
                user.email2user(mail_subject, mail_message)
                return render(request, 'confirm_signup.html')
    else:
        login_form = LoginForm()
        signup_form = SignupForm()

    return render(request, 'loginsignup.html', {'login_form': login_form, 'signup_form': signup_form})


def ActivateAccountView(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('profile')
    else:
        # invalid link
        return redirect('home')


@login_required(login_url='login')
def ProfileView(request):

    owner_rooms = Owner.objects.filter(user_id=request.user.pk) # Список владений помещениями
    activetab = 1  # Активная закладка

    if request.method == 'POST':
        avataruploadform = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
        emailchangeform = EmailChangeForm(request.POST, instance=request.user)
        sendownerrequestform = SendOwnerRequest(request.POST)

        if ('x' in request.POST) and ('y' in request.POST):
            if avataruploadform.is_valid():
                avataruploadform.save()
                return redirect('profile')

        if 'email-change-submit' in request.POST:
            if emailchangeform.is_valid():
                emailchangeform.save()
                return redirect('profile')

        if 'owner-request-submit' in request.POST:
            if sendownerrequestform.is_valid():
                owner = sendownerrequestform.save(commit=False)
                owner.user = request.user
                owner.save()
                return redirect('profile')

    else:
        avataruploadform = AvatarUploadForm()
        emailchangeform = EmailChangeForm(initial={'phone': request.user.phone})
        sendownerrequestform = SendOwnerRequest()

    return render(request, 'profile.html', {'avataruploadform': avataruploadform,
                                            'owner_rooms': owner_rooms,
                                            'emailchangeform': emailchangeform,
                                            'sendownerrequestform': sendownerrequestform,
                                            'activetab': activetab})
