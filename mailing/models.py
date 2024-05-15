from django.db import models
from django.utils import timezone
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    '''Класс клиент сервиса.'''
    email = models.EmailField(max_length=250, unique=True, verbose_name='Контактный Email')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['full_name',]

    def __str__(self):
        '''Добавляем строковое отображение.'''
        return f' {self.email} ({self.full_name})'


class Message(models.Model):
    '''Класс сообщение для рассылки.'''
    title = models.CharField(max_length=250, verbose_name='Тема письма')
    message = models.TextField(verbose_name='Тело письма', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор сообщения', **NULLABLE)

    class Meta:
        verbose_name = 'Cообщение'
        verbose_name_plural = 'Cообщения'

    def __str__(self):
        '''Добавляем строковое отображение.'''
        return f'{self.title} {self.message}'


class Mailing(models.Model):
    '''Класс рассылки сервиса.'''
    PERIODICITY = [
        ('daily', 'раз в день'),
        ('weekly', 'раз в неделю'),
        ('monthly', 'раз в месяц'),
    ]
    STATUS_CHOICES = [
        ('completed', 'завершена'),
        ('created', 'создана'),
        ('started', 'запущена'),
    ]
    name = models.CharField(max_length=100, default='рассылка', verbose_name='Наименование рассылки')
    client = models.ManyToManyField(Client, verbose_name='Клиент сервиса')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    started = models.DateTimeField(default=timezone.now, verbose_name='Дата начала рассылки')
    date_next = models.DateTimeField(default=timezone.now, verbose_name='Следующая дата рассылки')
    finished = models.DateTimeField(default=timezone.now, verbose_name='Дата окончания рассылки', **NULLABLE)
    periodicity = models.CharField(max_length=50, choices=PERIODICITY, default='daily',
                                   verbose_name='Периодичность рассылки')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created',
                              verbose_name='Статус рассылки')
    is_active = models.BooleanField(default=True, verbose_name='Активность рассылки')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['started',]
        permissions = [
            ('set_is_active', 'Активация рассылки')
        ]

    def __str__(self):
        '''Добавляем строковое отображение.'''
        return (f'{self.name}: дата начала рассылки - {self.started}, периодичность рассылки - {self.periodicity},'
                f'статус: {self.status}')


class Log(models.Model):
    '''Класс логи рассылки.'''
    mailing_name = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)
    last_mailing = models.DateTimeField(auto_now=True, verbose_name='Дата и время последней попытки')
    mail_status = models.CharField(max_length=100, verbose_name='Статус попытки', **NULLABLE)
    mail_response = models.CharField(max_length=100, verbose_name='Ответ почтового сервера', **NULLABLE)

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

    def __str__(self):
        '''Добавляем строковое отображение.'''
        return (f'Дата и время последней попытки: {self.last_mailing}.'
                f' Статус попытки: {self.mail_status}')
