import django_filters
from api.models import Ticket
from django.contrib.auth.models import User, Group


class TicketFilter(django_filters.FilterSet):

    @property
    def qs(self):
        qs = super(TicketFilter, self).qs
        if self.request.user.id:
            user = User.objects.get(id=self.request.user.id)
            admin_group = Group.objects.get(name='Administrador')
            tecnic_group = Group.objects.get(name='Técnico')
            customer_group = Group.objects.get(name='Cliente')

            if len(user.groups.all()) == 0 or customer_group in user.groups.all():
                return qs.filter(reporter_id=user.id)
            else:
                return qs
        else:
            return qs

    class Meta:
        model = Ticket
        fields = ['codename', 'type', 'title', 'priority', 'status', 'reporter', 'assignee']
