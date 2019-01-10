import csv
import xlwt
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.shortcuts import redirect, render, HttpResponse
from django_filters.views import FilterView
from django_tables2 import  RequestConfig
from django_tables2.views import SingleTableMixin
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from api.models import Ticket
from . import tables
from . import filters


class TicketListView(LoginRequiredMixin, FilterView):
    table_class = tables.TicketTable
    model = Ticket
    template_name = 'dashboard/index.html'
    filterset_class = filters.TicketFilter
    login_url = '/login'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TicketListView, self).get_context_data(**kwargs)
        context['table'] = tables.TicketTable(context['filter'].qs)
        RequestConfig(self.request).configure(context['table'])
        context['users'] = User.objects.all()
        return context


class TicketDetailView(generic.DetailView):
    model = Ticket
    template_name = 'dashboard/ticket.html'
    extra_context = {'users': User.objects.all()}


def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Cuenta creada correctamente.')
            return redirect('dashboard:register')

    else:
        f = UserCreationForm()

    return render(request, 'dashboard/register.html', {'form': f})


class UibitLoginView(LoginView):
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True


class UibitLogoutView(LogoutView):
    template_name = 'dashboard/logout.html'


def export_excel(self, *args, **kwargs):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="export.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Ticket')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['ID', 'Referencia', 'Tipo', 'Titulo', 'Descripcion', 'Prioridad', 'Estado', 'Creado', 'Modificado', 'Creador', 'Asignado']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    row_num += 1

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    ticket = Ticket.objects.get(id=kwargs['pk'])
    fields = ticket._meta.get_fields()
    fields = [field for field in fields if field.name != 'comments']
    ticket_values = []
    for field in fields:
        ticket_values.append(str(getattr(ticket, field.name)))
    row = ticket_values
    for col_num in range(len(row)):
        ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_csv(self, *args, **kwargs):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=export.csv'

    # opts = queryset.model._meta
    # field_names = [field.name for field in opts.fields]

    writer = csv.writer(response)
    # write a first row with header information
    # writer.writerow(field_names)

    # write data rows
    # I suggest you to check what output of `queryset`
    # because your `queryset` using `cursor.fetchall()`
    # print(queryset)
    ticket = Ticket.objects.get(id=kwargs['pk'])
    fields = ticket._meta.get_fields()
    fields = [field for field in fields if field.name != 'comments']
    for field in fields:
        writer.writerow([field.name, getattr(ticket, field.name)])

    return response
