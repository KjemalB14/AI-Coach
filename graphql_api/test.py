import unittest
from app import app


class GraphQLTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

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
        data = response.get_json()
        self.assertIn("data", data)
        self.assertEqual(data["data"]["hello"], "Hello, World!")


if __name__ == "__main__":
    unittest.main()
