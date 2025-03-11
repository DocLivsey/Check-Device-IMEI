import uuid

from pydantic import BaseModel

from CheckIMEI.models import Service, Property, IMEICheck


class ServiceResponse(BaseModel):
    title: str
    price: str

    @staticmethod
    def to_response(service: Service):
        return ServiceResponse(**service.dict())

    @staticmethod
    def from_data(data: dict):
        return ServiceResponse(**data)


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
    def to_response(properties: Property):
        return PropertiesResponse(**properties.dict())

    @staticmethod
    def from_data(data: dict):
        return PropertiesResponse(**data)


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
    def to_response(imei_check: IMEICheck):
        return IMEICheckResponse(**imei_check.dict())

    @staticmethod
    def from_data(data: dict):
        return IMEICheckResponse(**data)