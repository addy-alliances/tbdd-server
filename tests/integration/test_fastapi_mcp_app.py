import asyncio
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.mcp_app import app, mcp


class FastApiMcpAppTests(unittest.TestCase):
    def test_simulate_http_api_is_exposed_as_rest_api(self):
        expected = {
            "ok": True,
            "status_code": 200,
            "headers": {},
            "body": "ok",
            "json": None,
            "url": "https://example.test",
        }

        with patch(
            "src.controllers.simulator_apis._rest_api_simulator.execute",
            return_value=expected,
        ) as execute:
            with TestClient(app) as client:
                response = client.post(
                    "/api/v1/simulate-http",
                    json={"url": "https://example.test"},
                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)
        execute.assert_called_once()

    def test_simulate_http_api_is_exposed_as_mcp_tool(self):
        async def list_tool_names():
            return {tool.name for tool in await mcp.list_tools()}

        tool_names = asyncio.run(list_tool_names())

        self.assertIn("simulate_http_api", tool_names)


if __name__ == "__main__":
    unittest.main()