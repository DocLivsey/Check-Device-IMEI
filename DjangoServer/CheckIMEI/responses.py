import uuid

from pydantic import BaseModel

from CheckIMEI.models import Service, Property, IMEICheck


class ServiceResponse(BaseModel):
    title: str
    price: str

    @staticmethod
    def to_service_response(service: Service):
        return ServiceResponse(
            title=service.title,
            price=service.price
        )

    @staticmethod
    def from_data(data: dict):
        title = data['title'] if 'title' in data else 'Undefined'
        price = data['price'] if 'price' in data else 'Undefined'

        return ServiceResponse(
            title=title,
            price=price
        )


class PropertiesResponse(BaseModel):
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

    @staticmethod
    def from_data(data: dict):
        device_name = data['device_name'] if 'device_name' in data else 'Undefined'
        image = data['image'] if 'image' in data else 'Undefined'
        imei = data['imei'] if 'imei' in data else 'Undefined'
        est_purchase_date = data['est_purchase_date'] if 'est_purchase_date' in data else -1
        sim_lock = data['sim_lock'] if 'sim_lock' in data else False
        warranty_status = data['warranty_status'] if 'warranty_status' in data else 'Undefined'
        repair_coverage = data['repair_coverage'] if 'repair_coverage' in data else 'Undefined'
        technical_support = data['technical_support'] if 'technical_support' in data else 'Undefined'
        model_desc = data['model_desc'] if 'model_desc' in data else 'Undefined'
        demo_unit = data['demo_unit'] if 'demo_unit' in data else False
        refurbished = data['refurbished'] if 'refurbished' in data else False
        purchase_country = data['purchase_country'] if 'purchase_country' in data else 'Undefined'
        apple_region = data['apple_region'] if 'apple_region' in data else 'Undefined'
        fmi_on = data['fmi_on'] if 'fmi_on' in data else False
        lost_mode = data['lost_mode'] if 'lost_mode' in data else 'Undefined'
        usa_block_status = data['usa_block_status'] if 'usa_block_status' in data else 'Undefined'
        network = data['network'] if 'network' in data else 'Undefined'

        return PropertiesScheme(
            device_name=device_name,
            image=image,
            imei=imei,
            est_purchase_date=est_purchase_date,
            sim_lock=sim_lock,
            warranty_status=warranty_status,
            repair_coverage=repair_coverage,
            technical_support=technical_support,
            model_desc=model_desc,
            demo_unit=demo_unit,
            refurbished=refurbished,
            purchase_country=purchase_country,
            apple_region=apple_region,
            fmi_on=fmi_on,
            lost_mode=lost_mode,
            usa_block_status=usa_block_status,
            network=network,
        )


class IMEICheckResponse(BaseModel):
    id: str
    type: str
    status: str
    order_id: str
    service: ServiceResponse
    amount: str
    device_id: str
    processed_at: int
    properties: PropertiesResponse

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

    @staticmethod
    def from_data(data: dict):
        id = data['id'] if 'id' in data else str(uuid.uuid4())
        type = data['type'] if 'type' in data else 'Undefined'
        status = data['status'] if 'status' in data else 'Undefined'
        order_id = data['order_id'] if 'order_id' in data else 'Undefined'
        service = data['service'] if 'service' in data else {}
        amount = data['amount'] if 'amount' in data else 'Undefined'
        device_id = data['device_id'] if 'device_id' in data else 'Undefined'
        processed_at = data['processed_at'] if 'processed_at' in data else -1
        properties = data['properties'] if 'properties' in data else {}

        return IMEICheckResponse(
            id=id,
            type=type,
            status=status,
            order_id=order_id,
            service=ServiceResponse.to_service_response(service),
            amount=amount,
            device_id=device_id,
            processed_at=processed_at,
            properties=PropertiesResponse.to_properties_response(properties),
        )