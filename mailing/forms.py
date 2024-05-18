from django import forms
from django.forms import DateTimeInput
from mailing.models import Client, Mailing, Message


class StyleFormMixin:
    '''Класс стилизации формы'''
    def __init__(self, *args, **kwargs):
        '''Функция стилизации формы'''
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('owner',)


class MailingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        fields = '__all__'
        exclude = ('date_next', 'owner')

        widgets = {
            'start_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
        }


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        exclude = ('owner',)
