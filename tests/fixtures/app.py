# pyright: reportIncompatibleMethodOverride=false
# pyright:reportUnusedFunction=false
# pylint: disable=W0102
# pylint: disable=W0221
# pylint: disable=W0613

from typing import Dict, Any
from json import dumps
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from dotenv import find_dotenv, load_dotenv


from api.app import create_app


class Client(TestClient):

    def __init__(self, app: FastAPI):
        super().__init__(app)

    def get(
        self,
        url: str,
        headers: Dict[str, Any] = {},
        params: Dict[str, Any] = {},
    ):
        return super().get(url=url, headers={**self.headers, **headers}, params=params)

    def post(
        self,
        url: str,
        data: Dict[Any, Any] = {},
        headers: Dict[str, Any] = {},
        params: Dict[str, Any] = {},
    ):
        return super().post(
            url=url, data=dumps(data), headers={**self.headers, **headers}, params=params  # type: ignore
        )

    def patch(
        self,
        url: str,
        data: Dict[Any, Any] = {},
        headers: Dict[str, Any] = {},
        params: Dict[str, Any] = {},
    ):
        return super().patch(
            url=url, data=dumps(data), headers={**self.headers, **headers}, params=params  # type: ignore
        )

    def delete(
        self, url: str, headers: Dict[str, Any] = {}, params: Dict[str, Any] = {}
    ):
        return super().delete(
            url=url, headers={**self.headers, **headers}, params=params
        )


@pytest.fixture(scope="function")
def client():
    env = find_dotenv(".env.test")
    load_dotenv(env)
    app = create_app()

    yield Client(app)
