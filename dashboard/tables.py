import django_tables2 as tables
from api.models import Ticket


class TicketTable(tables.Table):

    codename = tables.LinkColumn('dashboard:ticket-detail', args=[tables.A('pk')])

    class Meta:
        model = Ticket
        template_name = 'django_tables2/bootstrap.html'
        fields = ('codename', 'type', 'title', 'priority', 'status', 'created_at', 'reporter', 'assignee')

