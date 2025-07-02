import unittest
import os
import json
import tempfile
from fastapi.testclient import TestClient
from app import app


class GraphQLAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Create a temporary test file
        self.test_video_fd, self.test_video_path = tempfile.mkstemp(
            suffix='.mp4')
        with os.fdopen(self.test_video_fd, 'wb') as f:
            f.write(b'test video content')

    def tearDown(self):
        # Clean up the temp file
        os.unlink(self.test_video_path)

    def test_hello_query(self):
        query = """
        {
            hello
        }
        """
        response = self.client.post(
            "/graphql",
            json={"query": query}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("data", data)
        self.assertEqual(data["data"]["hello"], "Hello, World!")

    def test_upload_video(self):
        with open(self.test_video_path, 'rb') as f:
            response = self.client.post(
                "/upload-video",
                files={"file": ("test.mp4", f, "video/mp4")}
            )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("filename", data)

    def test_video_list_query(self):
        query = """
        {
            videoList {
                filename
                uploadTime
            }
        }
        """
        response = self.client.post(
            "/graphql",
            json={"query": query}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("data", data)
        self.assertIn("videoList", data["data"])


if __name__ == "__main__":
    unittest.main()
