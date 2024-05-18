import random
import secrets
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        token = secrets.token_hex(16)
        user = form.save()
        user.token = token
        user.is_active = False
        user.save()
        host = self.request.get_host()
        link = f"http://{host}/users/confirm-register/{token}"
        message = f"Вы успешно зарегистрировались на нашей платформе, подтвердите почту по ссылке: {link}"
        send_mail(
            subject='Поздравляем с регистрацией',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def confirm_email(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = "".join([str(random.randint(0, 9) for _ in range(12))])
    send_mail(
        subject='Восстановление пароля',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('users:login'))


# def activate_user(request):
#     '''Функция активации пользователя.'''
#     key = request.GET.get('token')
#     current_user = User.objects.filter(is_active=False)
#     for user in current_user:
#         if str(user.token) == str(key):
#             user.is_active = True
#             user.token = None
#             user.save()
#     response = redirect(reverse_lazy('users:login'))
#     return response
#
#
# def generate_new_password(request):
#     '''Функция смены пароля.'''
#     new_password = get_new_password()
#     send_mail(
#         subject='Вы сменили пароль',
#         message=f'Ваш новый пароль: {new_password}',
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[request.user.email]
#     )
#     request.user.set_password(new_password)
#     request.user.save()
#
#     return redirect(reverse('users:login'))
#
#
# class ProfileView(UpdateView):
#     model = User
#     form_class = UserProfileForm
#     success_url = reverse_lazy('users:profile')
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#
# @login_required
# @permission_required(['users.view_user', 'users.set_is_active'])
# def get_users_list(request):
#     users_list = User.objects.all()
#     context = {
#         'object_list': users_list,
#         'title': 'Список пользователей сервиса',
#     }
#     return render(request, 'users/user_list.html', context)
#
#
# def toogle_activity(request, pk):
#     user_item = get_object_or_404(User, pk=pk)
#     if user_item.is_active:
#         user_item.is_active = False
#     else:
#         user_item.is_active = True
#     user_item.save()
#     return redirect('users:list_view')
