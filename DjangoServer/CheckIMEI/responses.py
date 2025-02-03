from CheckIMEI.models import Service, Property, IMEICheck


class ServiceResponse:
    title: str
    price: str

    def __init__(self, title: str, price: str) -> None:
        self.title = title
        self.price = price

    @staticmethod
    def to_service_response(service: Service):
        return ServiceResponse(
            title=service.title,
            price=service.price
        )


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

    def __init__(
            self,
            device_name: str,
            image: str,
            imei: str,
            est_purchase_date: int,
            sim_lock: bool,
            warranty_status: str,
            repair_coverage: str,
            technical_support: str,
            model_desc: str,
            demo_unit: bool,
            refurbished: bool,
            purchase_country: str,
            apple_region: str,
            fmi_on: bool,
            lost_mode: str,
            usa_block_status: str,
            network: str,
    ):
        self.device_name = device_name
        self.image = image
        self.imei = imei
        self.est_purchase_date = est_purchase_date
        self.sim_lock = sim_lock
        self.warranty_status = warranty_status
        self.repair_coverage = repair_coverage
        self.technical_support = technical_support
        self.model_desc = model_desc
        self.demo_unit = demo_unit
        self.refurbished = refurbished
        self.purchase_country = purchase_country
        self.apple_region = apple_region
        self.fmi_on = fmi_on
        self.lost_mode = lost_mode
        self.usa_block_status = usa_block_status
        self.network = network

    @staticmethod
    def to_properties_response(properties: Property):
        return PropertiesResponse(
            device_name=properties.device_name,
            image=properties.image,
            imei=properties.imei,
            est_purchase_date=properties.est_purchase_date,
            sim_lock=properties.sim_lock,
            warranty_status=properties.warranty_status,
            repair_coverage=properties.repair_coverage,
            technical_support=properties.technical_support,
            model_desc=properties.model_desc,
            demo_unit=properties.demo_unit,
            refurbished=properties.refurbished,
            purchase_country=properties.purchase_country,
            apple_region=properties.apple_region,
            fmi_on=properties.fmi_on,
            lost_mode=properties.lost_mode,
            usa_block_status=properties.usa_block_status,
            network=properties.network,
        )


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

    def __init__(
            self,
            id: str,
            type: str,
            status: str,
            order_id: str,
            service: ServiceResponse,
            amount: str,
            device_id: str,
            processed_at: int,
            properties: PropertiesResponse,
    ):
        self.id = id
        self.type = type
        self.status = status
        self.order_id = order_id
        self.service = service
        self.amount = amount
        self.device_id = device_id
        self.processed_at = processed_at
        self.properties = properties

    @staticmethod
    def to_imei_check_response(imei_check: IMEICheck):
        return IMEICheckResponse(
            id=str(imei_check.id),
            type=imei_check.type,
            status=imei_check.status,
            order_id=imei_check.order_id,
            service=ServiceResponse.to_service_response(imei_check.service),
            amount=imei_check.amount,
            device_id=imei_check.device_id,
            processed_at=imei_check.processed_at,
            properties=PropertiesResponse.to_properties_response(imei_check.properties),
        )