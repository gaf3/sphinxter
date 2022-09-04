import unittest
import unittest.mock

import sphinxter

class TestContent(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        content = sphinxter.Document.Content("people", "stuff", "things")

        self.assertEqual(content.module, "people")
        self.assertEqual(content.kind, "stuff")
        self.assertEqual(content.parsed, "things")


class TestDocument(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        document = sphinxter.Document("people", "stuff", "things", "thingies")

        self.assertEqual(document.path, "people")
        self.assertEqual(document.title, "stuff")
        self.assertEqual(document.toctree, "things")
        self.assertEqual(document.indent, "thingies")
        self.assertEqual(document.contents, {})

    def test_add(self):

        document = sphinxter.Document("people", "stuff", "things", "thingies")

        document.add("people", "stuff", "things", 7)

        self.assertEqual(document.contents[7][0].module, "people")
        self.assertEqual(document.contents[7][0].kind, "stuff")
        self.assertEqual(document.contents[7][0].parsed, "things")
