from fastapi import FastAPI
from fastmcp import FastMCP

from src.controllers.simulator_apis import api_app, api_router

mcp = FastMCP.from_fastapi(app=api_app, name="tbdd-server")
mcp_http_app = mcp.http_app(path="/")

app = FastAPI(
	title="tbdd-server",
	version="1.0.0",
	lifespan=mcp_http_app.lifespan,
)
app.include_router(api_router)
app.mount("/mcp", mcp_http_app)
