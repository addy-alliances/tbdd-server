from typing import Any

from fastapi import APIRouter, FastAPI

from src.controllers.models import SimulateHttpApiRequest
from src.simulators.rest_api_simulator import RestApiSimulator


api_app = FastAPI(title="tbdd-server API", version="1.0.0")
api_router = APIRouter()
_rest_api_simulator = RestApiSimulator()


@api_router.post(
    "/api/v1/simulate-http",
    operation_id="simulate_http_api",
    summary="Execute an HTTP API request",
)
def simulate_http_api(request: SimulateHttpApiRequest) -> dict[str, Any]:
    return _rest_api_simulator.execute(**request.model_dump())


api_app.include_router(api_router)