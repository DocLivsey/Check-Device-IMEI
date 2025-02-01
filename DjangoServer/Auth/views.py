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

        if not telegram_id:
            return Response({"error": "Telegram ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        profile = TelegramUser.objects.filter(telegram_id=telegram_id).first()

        if not profile:
            try:
                user = User.objects.create(username=f"tg@{telegram_id}")
            except IntegrityError:
                user = User.objects.get(username=f"tg@{telegram_id}")
            profile = TelegramUser.objects.create(user=user, telegram_id=telegram_id)
            user = profile.user
        else:
            user = profile.user

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'token': token.key,
                'telegram_id': telegram_id,
            }
        )