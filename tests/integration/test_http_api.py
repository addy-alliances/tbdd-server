import unittest

from src.service.simulator_service import execute_http_api


class HttpApiIntegrationTests(unittest.TestCase):
    def test_executes_get_request_against_google(self):
        result = execute_http_api(
            "https://www.google.com",
            method="GET",
            accept="text/html",
            timeout=10,
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["status_code"], 200)
        self.assertTrue(result["url"].startswith("https://www.google.com"))
        self.assertTrue(result["body"])


if __name__ == "__main__":
    unittest.main()