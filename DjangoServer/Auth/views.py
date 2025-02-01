from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from Auth.models import TelegramUser

class TelegramAuthView(APIView):

    def post(self, request):
        telegram_user = request.data.get('telegram_user')
        telegram_user_id = int(telegram_user.get('telegram_id'))
        telegram_user_username = telegram_user.get('telegram_username')

        if not telegram_user_id:
            return Response({"error": "Telegram ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        profile = TelegramUser.objects.filter(telegram_id=telegram_user_id).first()

        if not profile:
            if telegram_user_username:
                try:
                    user = User.objects.create(username=f"tg@{telegram_user_username}")
                except IntegrityError as error:
                    print(error)
                    user = User.objects.get(username=f"tg@{telegram_user_username}")
            else:
                try:
                    user = User.objects.create(username=f"tg@{telegram_user_id}")
                except IntegrityError:
                    user = User.objects.get(username=f"tg@{telegram_user_id}")
            profile = TelegramUser.objects.create(user=user, telegram_id=telegram_user_id)
            user = profile.user
        else:
            user = profile.user

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key
            }
        )