from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Ticket


class IndexView(generic.ListView):
    template_name = 'dashboard/index.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return []


class TicketDetailView(generic.DetailView):
    model = Ticket
    template_name = 'polls/ticket.html'
