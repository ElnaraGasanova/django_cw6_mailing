from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    preview = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    published_date = models.DateField(verbose_name='Дата публикации', **NULLABLE)
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.title} ({self.views_count} просмотров)'

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
