"""UI/integration tests: real HTTP server on a free port, real requests."""
import json, threading, unittest, urllib.request
from tests import helpers  # noqa: F401
from smart_campus.server import create_server


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = create_server(0)
        cls.base = "http://127.0.0.1:%d" % cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown(); cls.srv.server_close()

    def get(self, path):
        with urllib.request.urlopen(self.base + path) as r:
            return r.read().decode(), r.headers["Content-Type"]

    def post(self, path, payload):
        req = urllib.request.Request(self.base + path, json.dumps(payload).encode(),
                                     {"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())

    def test_page_is_served_and_is_responsive(self):
        html, ctype = self.get("/")
        self.assertIn("text/html", ctype)
        self.assertIn('name="viewport"', html)
        self.assertIn('id="rooms"', html)

    def test_filter_then_check_flow(self):
        rooms = json.loads(self.get("/api/rooms?participants=25&equipment=projector")[0])
        self.assertEqual([r["id"] for r in rooms["rooms"]], ["maple", "pine"])
        res = self.post("/api/check", {"room": "pine", "start": "700", "end": "760"})
        self.assertTrue(res["available"])

    def test_switching_rooms_changes_result(self):
        a = self.post("/api/check", {"room": "sunset", "start": "560", "end": "590"})
        b = self.post("/api/check", {"room": "maple", "start": "560", "end": "590"})
        self.assertTrue(a["available"]); self.assertFalse(b["available"])

    def test_empty_state_over_http(self):
        out = json.loads(self.get("/api/rooms?participants=999")[0])
        self.assertTrue(out["empty"])


if __name__ == "__main__":
    unittest.main()
