from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from Auth.models import TelegramUser

class TelegramAuthView(APIView):

    def post(self, request):
        telegram_id = int(request.data.get('telegram_id'))
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if not telegram_id:
            return Response({"error": "Telegram ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        profile = TelegramUser.objects.filter(telegram_id=telegram_id).first()

        if not profile:
            try:
                user = User.objects.create(
                    username=f"tg@{telegram_id}",
                    first_name=first_name,
                    last_name=last_name,
                )
            except IntegrityError:
                user = User.objects.get(
                    username=f"tg@{telegram_id}",
                    first_name=first_name,
                    last_name=last_name,
                )
            profile = TelegramUser.objects.create(user=user, telegram_id=telegram_id)
            user = profile.user
        else:
            user = profile.user
            
        if not user.is_active:
            return Response(
                {
                    "message": "User is not active"
                }, 
                status=status.HTTP_403_FORBIDDEN
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'token': token.key,
                'telegram_id': telegram_id,
            },
            status=status.HTTP_200_OK,
        )