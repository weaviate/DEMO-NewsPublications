import weaviate
import unittest

class Test(unittest.TestCase):
    def test_things(self):
        client = weaviate.Client("http://localhost:8080")

        all_things = client.data_object.get()
        self.assertGreaterEqual(all_things, 1)

    def test_get_articles(self):
        client = weaviate.Client("http://localhost:8080")

        query = "{Get {Things {Article {title url wordCount InPublication {... on Publication {name class}}}}}}"

        result = client.query.raw(query)

        self.assertGreaterEqual(result['data']['Get']['Things']['Article'], 1)