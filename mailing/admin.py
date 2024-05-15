from django.contrib import admin
from mailing.models import Client, Message, Mailing, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    '''Класс клиента сервиса в админке.'''
    list_display = ('pk', 'email', 'full_name',)
    list_filter = ('full_name',)
    search_fields = ('full_name', 'comment',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    '''Класс сообщение для рассылки в админке.'''
    list_display = ('pk', 'title', 'message',)
    list_filter = ('title',)
    search_fields = ('title', 'message',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    '''Класс рассылки сервиса в админке.'''
    list_display = ('pk', 'name', 'started', 'is_active',)
    list_filter = ('name',)
    search_fields = ('name', 'is_active',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    '''Класс логи рассылки в админке.'''
    list_display = ('pk', 'mailing_name', 'last_mailing', 'mail_status',)
    list_filter = ('mail_status',)
    search_fields = ('mailing_name', 'mail_status',)
