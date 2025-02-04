import uuid

from pydantic import BaseModel


class HelloScheme(BaseModel):
    message: str


def to_message(message: str) -> HelloScheme:
    if not message:
        message = 'Undefined'

    return HelloScheme(message=message)

class ServiceScheme(BaseModel):
    title: str
    price: str


def to_service(service_data: dict):
    title = service_data['title'] if 'title' in service_data else 'Undefined'
    price = service_data['price'] if 'price' in service_data else 'Undefined'

    return ServiceScheme(
        title=title,
        price=price
    )


class PropertiesScheme(BaseModel):
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


def to_properties(properties_data: dict):
    device_name = properties_data['device_name'] if 'device_name' in properties_data else 'Undefined'
    image = properties_data['image'] if 'image' in properties_data else 'Undefined'
    imei = properties_data['imei'] if 'imei' in properties_data else 'Undefined'
    est_purchase_date = properties_data['est_purchase_date'] if 'est_purchase_date' in properties_data else -1
    sim_lock = properties_data['sim_lock'] if 'sim_lock' in properties_data else False
    warranty_status = properties_data['warranty_status'] if 'warranty_status' in properties_data else 'Undefined'
    repair_coverage = properties_data['repair_coverage'] if 'repair_coverage' in properties_data else 'Undefined'
    technical_support = properties_data['technical_support'] if 'technical_support' in properties_data else 'Undefined'
    model_desc = properties_data['model_desc'] if 'model_desc' in properties_data else 'Undefined'
    demo_unit = properties_data['demo_unit'] if 'demo_unit' in properties_data else False
    refurbished = properties_data['refurbished'] if 'refurbished' in properties_data else False
    purchase_country = properties_data['purchase_country'] if 'purchase_country' in properties_data else 'Undefined'
    apple_region = properties_data['apple_region'] if 'apple_region' in properties_data else 'Undefined'
    fmi_on = properties_data['fmi_on'] if 'fmi_on' in properties_data else False
    lost_mode = properties_data['lost_mode'] if 'lost_mode' in properties_data else 'Undefined'
    usa_block_status = properties_data['usa_block_status'] if 'usa_block_status' in properties_data else 'Undefined'
    network = properties_data['network'] if 'network' in properties_data else 'Undefined'

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


class IMEICheckScheme(BaseModel):
    id: str
    type: str
    status: str
    order_id: str
    service: ServiceScheme
    amount: str
    device_id: str
    processed_at: int
    properties: PropertiesScheme


def to_imei_check(data: dict):
    id = data['id'] if 'id' in data else str(uuid.uuid4())
    type = data['type'] if 'type' in data else 'Undefined'
    status = data['status'] if 'status' in data else 'Undefined'
    order_id = data['order_id'] if 'order_id' in data else 'Undefined'
    service = data['service'] if 'service' in data else {}
    amount = data['amount'] if 'amount' in data else 'Undefined'
    device_id = data['device_id'] if 'device_id' in data else 'Undefined'
    processed_at = data['processed_at'] if 'processed_at' in data else -1
    properties = data['properties'] if 'properties' in data else {}

    return IMEICheckScheme(
        id=id,
        type=type,
        status=status,
        order_id=order_id,
        service=to_service(service),
        amount=amount,
        device_id=device_id,
        processed_at=processed_at,
        properties=to_properties(properties),
    )
