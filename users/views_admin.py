from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from rest_framework import status

class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        # Call the parent class's post method to handle the login logic
        response = super().post(request, *args, **kwargs)

        # Check if the user is an admin
        if self.user and self.user.is_superuser:
            return response  # If admin, return the response as is

        
        return Response(
            {"detail": "Only administrators are allowed to log in."},
            status=status.HTTP_403_FORBIDDEN,
        )
