from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket, TicketComment
from .serializers import TicketSerializer, TicketCommentSerializer
from django.http import Http404
from rest_framework.permissions import IsAuthenticated 




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
            serializer.save()
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
        ticket_comments = TicketComment.objects.filter(ticket_id=ticket_id, user_id=user_id)
        serializer = TicketCommentSerializer(ticket_comments, many=True)
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