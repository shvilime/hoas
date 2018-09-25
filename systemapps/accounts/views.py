from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from systemapps.accounts.forms import SignupForm, LoginForm

# Create your views here.

def loginsignup(request):
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
                signup_form.save()
                username = signup_form.cleaned_data.get('username')
                raw_password = signup_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
    else:
        login_form = LoginForm()
        signup_form = SignupForm()
    return render(request, 'loginsignup.html', {'login_form': login_form, 'signup_form': signup_form})
