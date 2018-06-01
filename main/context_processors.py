from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


def toploginform_processor(request):
    if request.method == 'POST':
        TopLoginForm = AuthenticationForm(data=request.POST)
        if TopLoginForm.is_valid():
            user = TopLoginForm.get_user()
            login(request, user)
    else:
        TopLoginForm = AuthenticationForm()

    return {'TopLoginForm': TopLoginForm}