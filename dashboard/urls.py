from django.urls import path
from .views import TicketListView, TicketDetailView, UibitLoginView, UibitLogoutView, register, export_excel, export_csv

app_name = 'dashboard'
urlpatterns = [
    path('', TicketListView.as_view(), name='index'),
    path('login/', UibitLoginView.as_view(), name='login'),
    path('logout/', UibitLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:pk>/download/excel', export_excel, name='export-excel'),
    path('tickets/<int:pk>/download/csv', export_csv, name='export-csv'),
]
