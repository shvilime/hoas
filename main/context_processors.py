from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

# ===== Процессор для передачи формы регистрации в основной шаблон ===== #
def toploginform_processor(request):
    if request.method == 'POST':
        TopLoginForm = AuthenticationForm(data=request.POST)
        if TopLoginForm.is_valid():
            user = TopLoginForm.get_user()
            if request.POST.get('rememberme', False):
                request.session.set_expiry(0)
            login(request, user)
    else:
        TopLoginForm = AuthenticationForm()

    return {'toploginform': TopLoginForm}
