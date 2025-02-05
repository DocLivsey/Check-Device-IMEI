import requests
import structlog
from pydantic import ValidationError
from fastapi import APIRouter, Request, HTTPException, status

from v1.functiontools import handle_401_response

logger = structlog.get_logger(__name__)

from v1.schemas.checkIMEI import IMEICheckScheme, to_imei_check
from settings import server_host, api_base_path, api_version, imei_check_api_token

check_imei_router = APIRouter()

DEFAULT_SERVICE_ID = 1


class Methods:
    POST = 'POST'
    GET = 'GET'


@check_imei_router.get('/', response_model=IMEICheckScheme)
async def check_imei(request: Request):
    logger.info(
        'Handle GET request to API for check device IMEI',
        request_headers=request.headers,
        request_body=await request.json(),
    )
    
    request_headers = request.headers
    request_body = await request.json()
    
    handle_401_response(request_headers)

    response = request_imei_check(request_headers, request_body)

    return to_imei_check(imei_check_response.json())


def request_imei_check(request_headers, request_body):
    url = f'{server_host}{api_base_path}{api_version}/check-imei/'
    imei_check_url = 'https://api.imeicheck.net/v1/checks'
    
    imei: str = request_body.get('imei')
    
    headers: dict = {
        'Authorization': request_headers.get('authorization'),
    }
    body: dict = {
        'imei': imei,
    }
    
    response: requests.Response
    try:
        response = handle_server_GET_request(url=url, headers=headers, body=body)
        
    except HTTPException as http_exception:
        if http_exception.status_code == status.HTTP_404_NOT_FOUND:
            logger.warning(
                'No such entry in the database for IMEI',
                imei=imei,
                endpoint=url,
                headers=headers,
                body=body,
            )
            
            imei_check_headers: dict = {
                'Authorization': f'Bearer {imei_check_api_token}'
            }
            imei_check_body: dict = {
                'deviceId': imei,
                'serviceId': DEFAULT_SERVICE_ID,
            }
            
            response = handle_imei_check_request(url=imei_check_url, headers=imei_check_headers, body=imei_check_body)
            body = response.json()
            
            response = handle_server_POST_request(url=url, headers=headers, body=body)
            
            if response.status_code == status.HTTP_201_CREATED:
                logger.info(
                    'Successfully saved entry about device in the database',
                    imei=imei,
                    endpoint=url,
                    headers=headers,
                    body=body,
                )
            
            else:
                logger.error(
                    'Failed to save entry about device in the database',
                    imei=imei,
                    endpoint=url,
                    headers=headers,
                    body=body,
                )
                
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Failed to save entry about device in the database',
                )
        
            


def handle_server_GET_request(url: str, headers: dict, body: dict) -> requests.Response:
    debug_log_text = 'Get data from bot`s request and trying to Send GET request to server`s REST to get info about device from database'
    return handle_request(url, headers, body, Methods.GET, debug_log_text)


def handle_server_POST_request(url: str, headers: dict, body: dict) -> requests.Response:
    debug_log_text = 'Sending data to server by POST request to save entry about device'
    return handle_request(url, headers, body, Methods.POST, debug_log_text)


def handle_imei_check_request(url: str, headers: dict, body: dict) -> IMEICheckScheme:
    dedug_log_text = 'Get data from bot`s request and trying to Send POST request to get info about device'
    response = handle_request(url, headers, body, Methods.POST, dedug_log_text)
    
    imei_data: IMEICheckScheme
    try:
        imei_data = to_imei_check(response.json())
        
    except ValidationError as validation_error:
        logger.error(
            'Failed to mapping from object to DTO',
            validation_error=str(validation_error),
            data=response.json(),
        )
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Failed to mapping from object {response.json()} to DTO',
        )
        
    return imei_data


def handle_request(
    url: str, 
    headers: dict, 
    body: dict,
    method: Methods,
    debug_log_txt: str
) -> requests.Response:
    response: requests.Response
    try:
        logger.debug(
            debug_log_txt,
            endpoint=url,
            headers=headers,
            body=body,
        )
        
        if method == Methods.GET:
            response = requests.get(
                url=imei_check_url,
                headers=headers,
                json=body,
            )
            
        elif method == Methods.POST:
            response = requests.post(
                url=imei_check_url,
                headers=headers,
                json=body,
            )
            
    except HTTPException as http_exception:
        logger.error(
            'HTTP error occurred',
            http_error=str(http_exception),
            endpoint=imei_check_url,
            headers=headers,
            body=body,
        )

        raise HTTPException(
            status_code=http_exception.status_code,
            detail=http_exception.detail,
        )

    except Exception as exception:
        logger.error(
            'Exception occurred',
            exc_info=exception,
            endpoint=url,
            headers=headers,
            body=body,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception),
        )
        
    if response.status_code != status.HTTP_200_OK:
        logger.error(
            'Failed to get data about device by IMEI',
            status_code=response.status_code,
            reason=response.reason,
            response=response.text,
            imei=imei,
        )

        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()
        )
        
    return response
