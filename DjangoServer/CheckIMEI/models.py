import uuid

from django.db import models


class CheckTypes:
    WEB = 'web'
    API = 'api'


class CheckStatuses:
    WAITING = 'waiting'
    PROCESSING = 'processing'
    SUCCESSFUL = 'successful'
    UNSUCCESSFUL = 'unsuccessful'
    FAILED = 'failed'


class Service(models.Model):
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=10)

    def dict(self):
        return {field[0]: field[1] for field in self.__dict__.items()}


class Property(models.Model):
    device_name = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    imei = models.CharField(max_length=15)
    est_purchase_date = models.IntegerField()
    sim_lock = models.BooleanField()
    warranty_status = models.CharField(max_length=100)
    repair_coverage = models.CharField(max_length=100)
    technical_support = models.CharField(max_length=100)
    model_desc = models.CharField(max_length=100)
    demo_unit = models.BooleanField()
    refurbished = models.BooleanField()
    purchase_country = models.CharField(max_length=100)
    apple_region = models.CharField(max_length=100)
    fmi_on = models.BooleanField()
    lost_mode = models.CharField(max_length=100)
    usa_block_status = models.CharField(max_length=100)
    network = models.CharField(max_length=100)

    def dict(self):
        return {field[0]: field[1] for field in self.__dict__.items()}


class IMEICheck(models.Model):
    TYPE_CHOICES = (
        (CheckTypes.WEB, 'web'),
        (CheckTypes.API, 'api'),
    )
    STATUS_CHOICES = (
        (CheckStatuses.WAITING, 'waiting'),
        (CheckStatuses.PROCESSING, 'processing'),
        (CheckStatuses.SUCCESSFUL, 'successful'),
        (CheckStatuses.UNSUCCESSFUL, 'unsuccessful'),
        (CheckStatuses.FAILED, 'failed'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES
    )
    order_id = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='checks'
    )
    amount = models.CharField(max_length=100)
    device_id = models.CharField(max_length=15)
    processed_at = models.IntegerField()
    properties = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='checks'
    )

    def dict(self):
        return {field[0]: field[1] for field in self.__dict__.items()}
