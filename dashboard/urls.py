from django.urls import path
from .views import IndexView, TicketDetailView

app_name = 'dashboard'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:ticket_id>/', TicketDetailView.as_view(), name='ticket')
]
