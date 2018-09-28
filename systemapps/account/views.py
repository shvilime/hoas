from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from systemapps.account.forms import SignupForm, LoginForm


# Create your views here.

def LoginSignupView(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        signup_form = SignupForm(data=request.POST)
        if 'login-form-submit' in request.POST:
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
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

                # username = signup_form.cleaned_data.get('email')
                # raw_password = signup_form.cleaned_data.get('password1')
                # user = authenticate(username=username, password=raw_password)
                # login(request, user)
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

def ProfileView(request):
    return render(request, 'profile.html')