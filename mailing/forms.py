from django import forms
from django.forms import DateTimeInput
from mailing.models import Client, Mailing, Message


class StyleFormMixin:
    '''Класс стилизации формы'''
    def __init__(self, *args, **kwargs):
        '''Функция стилизации формы'''
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)


class MailingForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(owner=user)
        self.fields['message'].queryset = Message.objects.filter(owner=user)

    class Meta:
        model = Mailing
        exclude = ('date_next', 'is_active', 'owner')

        widgets = {
            'start_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
        }


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)
