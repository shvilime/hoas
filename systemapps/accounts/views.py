from django.shortcuts import render
from systemapps.accounts.forms import SignupForm, LoginForm

# Create your views here.

def loginsignup(request):
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        signupform = SignupForm(request.POST)
        if loginform.is_valid():
            return
    else:
        loginform = LoginForm()
        signupform = SignupForm()
    return render(request, 'loginsignup.html', {'form': loginform})
