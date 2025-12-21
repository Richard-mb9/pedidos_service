# pylint: disable=W0613
from typing import Dict
from http import HTTPStatus
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from domain.enums import ErrorCategory

from domain.exceptions import DomainException

from .routes import create_routes

URL_PREFIX = ""
API_DOC = f"{URL_PREFIX}/doc/api"
API_DOC_REDOC = f"{URL_PREFIX}/doc/redoc"
API_DOC_JSON = f"{URL_PREFIX}/doc/api.json"
API_VERSION = "V1.0.0"


def create_app():
    api = FastAPI(
        title="Pedidos Service",
        description="Api for manage Orders",
        openapi_url=API_DOC_JSON,
        redoc_url=API_DOC_REDOC,
        docs_url=API_DOC,
        version=API_VERSION,
    )

    return create_routes(api, URL_PREFIX)


app = create_app()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


STATUS_CODE_MAP: Dict[ErrorCategory, int] = {
    ErrorCategory.NOT_FOUND: 404,
    ErrorCategory.CONFLICT: 409,
    ErrorCategory.VALIDATION: 422,
    ErrorCategory.FORBIDDEN: 403,
    ErrorCategory.INTERNAL: 500,
}


@app.exception_handler(DomainException)
def http_exception_handler(request: Request, error: DomainException):
    return JSONResponse(
        content={"detail": error.message}, status_code=STATUS_CODE_MAP[error.category]
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    response = {}
    for error in errors:
        key = error["loc"][1]
        response[key] = error["msg"]
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={"detail": response},
    )
