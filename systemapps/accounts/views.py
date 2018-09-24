from django.shortcuts import render
from systemapps.accounts.forms import SignupForm, LoginForm

# Create your views here.

def loginsignup(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        signup_form = SignupForm(request.POST)
        if 'login-form-submit' in request.POST:
            if login_form.is_valid():
                return
        if 'signup-form-submit' in request.POST:
            if signup_form.is_valid():
                return
    else:
        login_form = LoginForm()
        signup_form = SignupForm()
    return render(request, 'loginsignup.html', {'login_form': login_form, 'signup_form': signup_form})
