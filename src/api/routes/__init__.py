import os
from importlib import util
from pathlib import Path
from fastapi import FastAPI, APIRouter
from fastapi.openapi.utils import get_openapi

health_router = APIRouter()


@health_router.get("/health")
def ping():
    return "ok"  # pragma: no cover


def create_routes(app: FastAPI, url_prefix: str):
    app.include_router(health_router, prefix=f"{url_prefix}", tags=["health"])

    routes_directory = Path(__file__).parent

    for filename in os.listdir(routes_directory):
        if filename.endswith(".py") and filename not in [
            "__init__.py",
        ]:
            module_name = filename[:-3]
            module_path = f"{routes_directory}/{filename}"

            spec = util.spec_from_file_location(module_name, str(module_path))
            module = util.module_from_spec(spec)  # type: ignore
            spec.loader.exec_module(module)  # type: ignore

            if hasattr(module, "router"):
                router = getattr(module, "router")
                app.include_router(
                    router,
                    prefix=f"{url_prefix}/{module_name}",
                    tags=[module_name.replace("_", "").capitalize()],
                )

    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get("paths", {}).items():
            for _, param in method_item.items():
                responses = param.get("responses")
                # remove 422 response, also can remove other status code
                if "422" in responses:
                    del responses["422"]

    return app
