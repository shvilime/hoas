from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, is_safe_url
from django.utils.encoding import force_bytes, force_text
from django.views import View
from django.contrib import messages
from .tokens import account_activation_token
from .forms import *
from area.models import Owner
from area.forms import SendOwnerRequestForm
from area.services import *
from counter.models import CounterValue
from counter.forms import SendCounterValueForm


# ======================= Вход в систем, регистрация нового пользователя ==========================
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


# ======================= Активация пользователя по высланной ссылке ==============================
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


# ======================= Просмотр и редактирование профиля пользователя ==========================
class ProfileView(View):
    tablist = {'profile': 1,
               'area': 2,
               'car': 3,
               'resource': 4}
    template_name = 'profile.html'
    context = {'avataruploadform': AvatarUploadForm,
               'phonechangeform': EmailChangeForm,
               'sendownerrequestform': SendOwnerRequestForm,
               'sendcountervalueform': SendCounterValueForm,
               'activetab': tablist['profile']}

    def dispatch(self, request, *args, **kwargs):
        self.context['activetab'] = kwargs.get('activetab', self.tablist['profile'])
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.context['avataruploadform'] = AvatarUploadForm()
        self.context['phonechangeform'] = EmailChangeForm(initial={'phone': request.user.phone})
        self.context['sendownerrequestform'] = SendOwnerRequestForm(user=request.user)
        self.context['sendcountervalueform'] = SendCounterValueForm(user=request.user)
        self.context['counter_values'] = CounterValue.objects.filter(
            room__in=[item.room for item in
                      owner_requests_history(request.user, active=True)])  # Список поданных показаний
        self.context['owner_rooms'] = owner_requests_history(request.user)  # История заявок на право собственности

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        if ('x' in request.POST) and ('y' in request.POST):  # Форма по изменению аватара
            self.context['avataruploadform'] = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
            if self.context['avataruploadform'].is_valid():
                self.context['avataruploadform'].save()
                messages.success(request, 'Аватар обновлен', 'icon-ok-sign')
                return redirect('account:profile')
        if 'name-editphone-submit' in request.POST:  # Форма по изменению телефона
            self.context['phonechangeform'] = EmailChangeForm(request.POST, instance=request.user)
            if self.context['phonechangeform'].is_valid():
                self.context['phonechangeform'].save()
                messages.info(request, 'Номер телефона обновлен', 'icon-phone')
                return redirect('account:profile')
        if 'name-ownerrequest-submit' in request.POST:  # Форма по отправке заявки владельца
            self.context['sendownerrequestform'] = SendOwnerRequestForm(request.POST, user=request.user)
            self.context['activetab'] = self.tablist['area']
            if self.context['sendownerrequestform'].is_valid():
                owner = self.context['sendownerrequestform'].save(commit=False)
                owner.user = request.user
                owner.save()
                messages.success(request, 'Запрос отправлен', 'icon-ok-sign')
                return redirect('account:profile', activetab=self.context['activetab'])
        if 'name-countervalue-submit' in request.POST:  # Форма по подаче показания счетчика
            self.context['sendcountervalueform'] = SendCounterValueForm(request.POST, user=request.user)
            self.context['activetab'] = self.tablist['resource']
            if self.context['sendcountervalueform'].is_valid():
                value = self.context['sendcountervalueform'].save(commit=False)
                value.user = request.user
                value.save()
                messages.success(request, 'Показания переданы', 'icon-ok-sign')
                return redirect('account:profile', activetab=self.context['activetab'])

        return render(request, self.template_name, self.context)


