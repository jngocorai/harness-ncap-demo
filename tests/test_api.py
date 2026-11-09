import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class ApiTests(unittest.TestCase):
    def test_health(self):
        self.assertEqual(client.get("/health").json(), {"status": "ok"})

    def test_version(self):
        data = client.get("/version").json()
        self.assertEqual(data["mode"], "demo")
        self.assertTrue(data["version"])

    def test_long_prices(self):
        response = client.post("/preview", json={"direction": "LONG", "signal_price": 100})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for key, value in {"stop": 99.7, "tp1": 100.6, "tp2": 101}.items():
            self.assertAlmostEqual(data[key], value)

    def test_short_prices(self):
        data = client.post("/preview", json={"direction": "SHORT", "signal_price": 100}).json()
        for key, value in {"stop": 100.3, "tp1": 99.4, "tp2": 99}.items():
            self.assertAlmostEqual(data[key], value)

    def test_invalid_prices(self):
        for price in (0, -1, "NaN", "Infinity", "-Infinity", "invalid"):
            with self.subTest(price=price):
                self.assertEqual(client.post("/preview", json={
                    "direction": "LONG", "signal_price": price}).status_code, 422)

    def test_invalid_direction(self):
        self.assertEqual(client.post("/preview", json={
            "direction": "BUY", "signal_price": 100}).status_code, 422)

    def test_missing_price(self):
        self.assertEqual(client.post("/preview", json={"direction": "LONG"}).status_code, 422)

if __name__ == "__main__":
    unittest.main()

