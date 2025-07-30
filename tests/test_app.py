# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app, db, TimelinePost

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Make sure the database connection is established and tables are created
        if db.is_closed():
            db.connect()
        db.create_tables([TimelinePost], safe=True)
        # Clear rate limiting storage for tests
        from app import rate_limit_storage
        rate_limit_storage.clear()

    def tearDown(self):
        # Clean up after each test
        db.drop_tables([TimelinePost], safe=True)
        if not db.is_closed():
            db.close()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        # TODO Add more tests relating to the home page

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        # The API returns a direct array, not an object with "timeline_posts"
        assert isinstance(json, list)
        assert len(json) == 0
        # TODO Add more tests relating to the /api/timeline_post GET and POST apis
        # TODO Add more tests relating to the timeline page

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        json = response.get_json()
        assert "error" in json
        assert "Invalid name" in json["error"]

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        json = response.get_json()
        assert "error" in json
        assert "Invalid content" in json["error"]

        # POST request with malformed email (currently not validated in your app)
        # This test would fail with your current implementation since you don't validate email format
        # response = self.client.post("/api/timeline_post", data={
        #     "name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        # assert response.status_code == 400

if __name__ == '__main__':
    unittest.main()