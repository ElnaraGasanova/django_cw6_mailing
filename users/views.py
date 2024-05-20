import random
import secrets
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from mailing.models import Mailing
from users.forms import UserRegisterForm, UserUpdateView
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        token = secrets.token_hex(8)
        user = form.save()
        user.token = token
        user.is_active = False
        user.save()
        host = self.request.get_host()
        link = f"http://{host}/users/confirm-register/{token}"
        message = f"Вы успешно зарегистрировались, подтвердите почту по ссылке: {link}"
        send_mail(
            subject='Регистрация пройдена.',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def confirm_email(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    response = redirect(reverse_lazy('users:login'))
    return response


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserUpdateView

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    send_mail(
        subject='Восстановление пароля',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('users:login'))

@login_required
@permission_required('mailing.set_is_active')
def toogle_activity(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.is_active:
        mailing_item.is_active = False
    else:
        mailing_item.is_active = True
    mailing_item.save()
    return redirect(reverse('mailing:mailing_list'))


class VerifyCodeView(View):
    model = User
    template_name = 'users/genpassword.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        new_password = request.POST.get('new_password')
        user = User.objects.filter(verify_code=new_password).first()
        if user:
            user.is_verified = True
            user.save()
            return redirect('users:login')

        return redirect('users:new_password')

@login_required
@permission_required(['users.view_user', 'users.set_is_active'])
def get_users_list(request):
    users_list = User.objects.all()
    context = {
        'object_list': users_list,
        'title': 'Список пользователей сервиса',
    }
    return render(request, 'users/login.html', context)
