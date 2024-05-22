from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from blog.models import Blog
from mailing.forms import MailingForm, ClientForm, MessageForm
from mailing.models import Mailing, Client, Message, Log


class MailingListView(LoginRequiredMixin, ListView):
    '''Класс всех рассылок.'''
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MailingDetailView(DetailView):
    '''Класс просмотра рассылки.'''
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    '''Класс создания новой рассылки.'''
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    '''Класс редактирования рассылки.'''
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or self.request.user.is_superuser:
            return MailingForm
        else:
            return self.get_form_class()


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    '''Класс удаления рассылки.'''
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class ClientListView(ListView):
    '''Класс всех клиентов сервиса.'''
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    '''Класс создания нового клиента сервиса.'''
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    '''Класс редактирования клиента сервиса.'''
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientDeleteView(DeleteView):
    '''Класс удаления клиента сервиса.'''
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class MessageListView(ListView):
    '''Класс всех сообщений рассылок.'''
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    '''Класс создания нового сообщения рассылки.'''
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    '''Класс редактирования сообщения рассылки.'''
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(DeleteView):
    '''Класс удаления сообщения рассылки.'''
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class IndexView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = Blog.objects.all()[:3]
        context['object_list'] = Mailing.objects.all()

        unique_clients_count = Client.objects.all().values('email').distinct().count()
        context['unique_clients_count'] = unique_clients_count

        active_mailing_count = Mailing.objects.filter(is_active=True).count()
        context['active_mailing_count'] = active_mailing_count
        return context


def contacts(request):
    context = {
        'title': 'Контакты',
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"{name} ({phone}, {email}): {message}")

    return render(request, 'mailing/contacts.html', context)


class LogListView(ListView):
    model = Log
    success_url = reverse_lazy('mailing:mailing_list')
