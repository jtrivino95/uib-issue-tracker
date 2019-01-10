from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):
    codename = models.CharField(max_length=255, verbose_name='Referencia')
    type = models.CharField(
        max_length=255,
        choices=[
            ('issue', 'Incidencia'),
            ('request', 'Petición'),
            ('system', 'Sistemas'),
        ],
        verbose_name='Tipo'
    )
    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    priority = models.CharField(
        max_length=255,
        default='low',
        choices=[
            ('low', 'Baja'),
            ('middle', 'Media'),
            ('high', 'Alta'),
            ('severe', 'Grave'),
            ('critical', 'Crítica'),
        ],
        verbose_name='Prioridad'
    )
    status = models.CharField(
        max_length=255,
        choices=[
            ('new', 'Nuevo'),
            ('assigned', 'Asignado'),
            ('in-progress', 'En proceso'),
            ('solved', 'Resuelto'),
        ],
        default='new',
        verbose_name='Estado'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter', verbose_name='Creador')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='assignee', verbose_name='Asignado a')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.codename = \
            self.__get_code(self.type) + '-' + str(self.__class__.objects.latest('id').id) \
            if self.__class__.objects.count() > 0 else \
            self.__get_code(self.type) + '-' + "1"
        super(Ticket, self).save(force_insert, force_update, using, update_fields)


    @staticmethod
    def __get_code(type):
        if type == 'issue':
            return 'INC'
        elif type == 'request':
            return 'PET'
        elif type == 'system':
            return 'SYS'
        else:
            raise Exception


class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')

