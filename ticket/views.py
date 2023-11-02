from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket, TicketComment
from .serializers import TicketSerializer, TicketCommentSerializer, TicketCommentViewSerializer
from django.http import Http404
from rest_framework.permissions import IsAuthenticated 
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings 



class TicketListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter the queryset to only the request user's tickets.
        tickets = Ticket.objects.filter(user=self.request.user)
        return tickets

    def get(self, request):
        serializer = TicketSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        # Get the authenticated user directly from the request
        authenticated_user = request.user.id

        # Add the authenticated user to the serializer data
        serializer = TicketSerializer(data={**request.data, 'user': authenticated_user})

        if serializer.is_valid():
            ticket = serializer.save()            
            print("Ticket created!!")
            print(ticket)
            # ticket = Ticket.objects.get(id=ticket.data.)
            # Render the HTML email template
            email_subject = "New Ticket Notification"
            email_body = render_to_string('ticket/ticket_new.html', {'ticket': ticket, 'user': request.user.email})
            
        
            send_mail(
                        email_subject,
                        email_body,
                        settings.DEFAULT_FROM_EMAIL,  # Sender's email address
                        [request.user.email],           # Recipient's email address (user's email)
                        fail_silently=False,          # Set to True to suppress exceptions if sending fails
                        html_message=email_body,      # Set the HTML content here
                    )

            # Render the HTML email template
            email_subject_admin = "@admin: Ticket New Notification"
            email_body_admin = render_to_string('ticket/ticket_new.html', {'ticket': ticket, 'user': request.user.email})
                                
            send_mail(
            email_subject_admin,
            email_body_admin,
            settings.DEFAULT_FROM_EMAIL,  # Sender's email address
            [settings.ADMIN_EMAILS],           # Recipient's email address (user's email)
            fail_silently=False,          # Set to True to suppress exceptions if sending fails
            html_message=email_body_admin,      # Set the HTML content here
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketDetailView(APIView):
    def get_object(self, pk):
        try:
            return Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        ticket = self.get_object(pk)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)



# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from .models import TicketComment
# from .serializers import TicketCommentSerializer

class TicketCommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, ticket_id):
        user_id = request.user.id
        ticket_comments = TicketComment.objects.filter(ticket_id=ticket_id)
        serializer = TicketCommentViewSerializer(ticket_comments, many=True)
        return Response(serializer.data)

    def post(self, request, ticket_id):
        authenticated_user = request.user
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

        data = {**request.data, 'user': authenticated_user.id, 'ticket': ticket_id}

        serializer = TicketCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(request.data)
                       
            # Render the HTML email template
            email_subject_admin = "@admin: Comment Notification"
            email_body_admin = render_to_string('ticket/ticket_update.html', {'ticket': ticket, 'comment': request.data.get('content'), 'user': authenticated_user.email})
                                
            send_mail(
            email_subject_admin,
            email_body_admin,
            settings.DEFAULT_FROM_EMAIL,  # Sender's email address
            [settings.ADMIN_EMAILS],           # Recipient's email address (user's email)
            fail_silently=False,          # Set to True to suppress exceptions if sending fails
            html_message=email_body_admin,      # Set the HTML content here
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketCommentDetailView(APIView):
    def get_object(self, pk):
        try:
            return TicketComment.objects.get(pk=pk)
        except TicketComment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        ticket_comment = self.get_object(pk)
        serializer = TicketCommentSerializer(ticket_comment)
        return Response(serializer.data)