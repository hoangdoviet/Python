import enum
from typing import Union
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette import status
from pydantic import ValidationError
from app.schemas.base import ResponseSchemaBase
from app.resources import strings


class ExceptionType(enum.Enum):
    MS_UNAVAILABLE = status.HTTP_500_INTERNAL_SERVER_ERROR, '990', strings.MS_UNAVAILABLE
    MS_INVALID_API_PATH = status.HTTP_500_INTERNAL_SERVER_ERROR, '991', strings.MS_INVALID_API_PATH
    DATA_RESPONSE_MALFORMED = status.HTTP_500_INTERNAL_SERVER_ERROR, '992', strings.DATA_RESPONSE_MALFORMED

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, http_code, code, message):
        self.http_code = http_code
        self.code = code
        self.message = message


class CustomException(Exception):
    http_code: int
    message: str

    def __init__(self, http_code: int = None, message: str = None):
        self.http_code = http_code if http_code else status.HTTP_500_INTERNAL_SERVER_ERROR
        self.message = message


async def http_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.http_code,
        content=jsonable_encoder(
            ResponseSchemaBase().error_response(
                request,
                {
                    "code": exc.http_code,
                    "message": exc.message
                }
            )
        )
    )


async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            ResponseSchemaBase().error_response(
                request,
                {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": get_message_validation(exc)
                }
            )
        )
    )


async def fastapi_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            ResponseSchemaBase().error_response(
                request,
                {
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": strings.DATA_RESPONSE_MALFORMED
                }
            )
        )
    )

async def http422_error_handler(request: Request, exc: Union[RequestValidationError, ValidationError]):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            ResponseSchemaBase().error_response(
                request,
                {
                    "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                    "message": exc.errors()
                }
            )
        )
    )


def get_message_validation(exc):
    message = ""
    for error in exc.errors():
        message += "/'" + str(error.get("loc")[1]) + "'/" + ': ' + error.get("msg") + ", "

    message = message[:-2]

    return message
