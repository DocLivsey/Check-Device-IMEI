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
    
    @staticmethod
    def to_response(data: dict):
        return ServiceScheme(**data)


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
    
    @staticmethod
    def to_response(data: dict):
        return PropertiesScheme(**data)


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
    
    @staticmethod
    def to_response(data: dict):
        return IMEICheckScheme(**data)
