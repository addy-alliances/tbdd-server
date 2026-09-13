import unittest
from unittest.mock import patch

import httpx

from src.service.simulator_service import execute_http_api


class ExecuteHttpApiTests(unittest.TestCase):
    @patch("src.service.simulator_service.httpx.request")
    def test_execute_http_api_behaviors(self, request):
        with self.subTest("returns response metadata"):
            response = httpx.Response(
                200,
                json={"message": "ok"},
                request=httpx.Request("POST", "https://example.test/items"),
            )
            request.return_value = response

            result = execute_http_api(
                "https://example.test/items",
                method="post",
                json_body={"name": "item"},
                accept="application/json",
            )

            request.assert_called_once()
            call_kwargs = request.call_args.kwargs
            self.assertEqual(call_kwargs["method"], "POST")
            self.assertEqual(call_kwargs["json"], {"name": "item"})
            self.assertEqual(call_kwargs["headers"]["Accept"], "application/json")
            self.assertTrue(result["ok"])
            self.assertEqual(result["status_code"], 200)
            self.assertEqual(result["json"], {"message": "ok"})

        with self.subTest("rejects duplicate bodies"):
            with self.assertRaisesRegex(ValueError, "either 'body' or 'json_body'"):
                execute_http_api(
                    "https://example.test/items",
                    body="raw",
                    json_body={"name": "item"},
                )

        with self.subTest("returns HTTP errors"):
            request.reset_mock(side_effect=True)
            request.side_effect = httpx.ConnectError("connection refused")

            result = execute_http_api("https://example.test/items")

            self.assertFalse(result["ok"])
            self.assertIsNone(result["status_code"])
            self.assertEqual(result["error"]["type"], "ConnectError")


if __name__ == "__main__":
    unittest.main()