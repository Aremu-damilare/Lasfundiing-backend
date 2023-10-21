from django.urls import path
from .views_admin import TicketListCreateView, TicketDetailView, TicketCommentListCreateView, TicketCommentDetailView

urlpatterns = [
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    
    path('ticket/<int:ticket_id>/comments/', TicketCommentListCreateView.as_view(), name='ticket-comment-list-create'),
    # path('ticket-comments/<int:pk>/', TicketCommentDetailView.as_view(), name='ticket-comment-detail'),

]
