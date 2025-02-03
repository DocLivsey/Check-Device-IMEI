from django.db import OperationalError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            call_user = 'Anonymous'

            if user.first_name:
                call_user = user.first_name

            elif user.last_name:
                call_user = user.last_name

            elif user.username:
                call_user = user.username

            return Response({'message': f'Hello, {call_user}!'})

        except OperationalError:
            return Response({'message': 'Who are you?'})
