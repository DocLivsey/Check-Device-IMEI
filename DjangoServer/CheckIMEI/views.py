from django.db import OperationalError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            return Response({'message': f'Hello, {user.username}!'})
        except OperationalError:
            return Response({'message': 'Who are you?'})
