from django.db import OperationalError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from CheckIMEI.models import IMEICheck
from CheckIMEI.responses import IMEICheckResponse


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


class IMEICheckView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            imei = request.data['imei']

            device_data = IMEICheck.objects.filter(device_id=imei)
            imei_check_response = IMEICheckResponse.to_response(device_data)

            return Response(
                {'IMEICheckResponse': imei_check_response},
                status=status.HTTP_200_OK
            )

        except KeyError:
            return Response(
                {'message': 'No IMEI or wrong IMEI entry'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as exception:
            return Response(
                {'message': str(exception)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        imei_check: IMEICheck
        imei_check_response: IMEICheckResponse
        try:
            imei_check_response = IMEICheckResponse.from_data(request.data)

            imei_check = IMEICheck.objects.create(
                id=imei_check_response.id,
                type=imei_check_response.type,
                status=imei_check_response.status,
                order_id=imei_check_response.order_id,
                service=imei_check_response.service,
                amount=imei_check_response.amount,
                processed_at=imei_check_response.processed_at,
                properties=imei_check_response.properties,
            )
            imei_check.save()

            imei_check_response = IMEICheckResponse.to_response(imei_check)
        except Exception as exception:
            return Response(
                {'message': str(exception)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'IMEICheckResponse': imei_check_response},
            status=status.HTTP_201_CREATED
        )