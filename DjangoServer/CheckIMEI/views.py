from django.db import OperationalError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from CheckIMEI.models import CheckIMEI


class ServiceResponse:
    title: str
    price: str


class PropertiesResponse:
    device_name: str
    image: str
    imei: str
    est_purchase_date: int
    sim_lock: bool
    warranty_status: str
    repair_coverage: str
    technical_support: str
    model_desc: str
    demo_unit: bool
    refurbished: bool
    purchase_country: str
    apple_region: str
    fmi_on: bool
    lost_mode: str
    usa_block_status: str
    network: str


class IMEICheckResponse:
    id: str
    type: str
    status: str
    order_id: str
    service: ServiceResponse
    amount: str
    device_id: str
    processed_at: int
    properties: PropertiesResponse


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

            device_data = CheckIMEI.objects.filter(device_id=imei)

        except KeyError:
            return Response({'message': 'No IMEI or wrong IMEI entry'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        pass