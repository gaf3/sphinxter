import unittest
import unittest.mock

import sphinxter
from test import example
from test.test_sphinxter.test_reader import TestReader
from test.test_sphinxter.test_writer import TestWriter

class TestContent(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        content = sphinxter.Content("people", "stuff", "things")

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


class TestSphinxter(unittest.TestCase):

    maxDiff = None

    def test___init__(self):

        # defaults

        instance = sphinxter.Sphinxter("people")

        self.assertEqual(instance.modules, ["people"])
        self.assertEqual(instance.base, "docs/source")
        self.assertEqual(instance.indent, '    '
        )

        # values

        instance = sphinxter.Sphinxter("people", "stuff", "things", "stuffins", "thingies")

        self.assertEqual(instance.modules, ["people"])
        self.assertEqual(instance.titles, "stuff")
        self.assertEqual(instance.toctree, "things")
        self.assertEqual(instance.base, "stuffins")
        self.assertEqual(instance.indent, "thingies")

    def test_document(self):

        parsed = {}

        instance = sphinxter.Sphinxter("people")

        # empty

        instance.document("stuff", "things", parsed)

        self.assertEqual(instance.documents["index"].path, "docs/source/index.rst")
        self.assertEqual(instance.documents["index"].title, "stuff")
        self.assertTrue(instance.documents["index"].toctree)
        self.assertEqual(instance.documents["index"].indent, '    ')
        self.assertEqual(instance.documents["index"].contents[0][0].module, "stuff")
        self.assertEqual(instance.documents["index"].contents[0][0].kind, "things")
        self.assertEqual(instance.documents["index"].contents[0][0].parsed, parsed)

        # skip

        parsed = {
            "sphinx": False
        }

        instance.document("stuff", "things", parsed)

        self.assertEqual(len(instance.documents["index"].contents[0]), 1)

        # str

        parsed = {
            "sphinx":  "str",
        }

        instance.document("stuffins", "thingies", parsed)

        self.assertEqual(instance.documents["str"].path, "docs/source/str.rst")
        self.assertEqual(instance.documents["str"].title, "str")
        self.assertFalse(instance.documents["str"].toctree)
        self.assertEqual(instance.documents["str"].contents[0][0].module, "stuffins")
        self.assertEqual(instance.documents["str"].contents[0][0].kind, "thingies")
        self.assertEqual(instance.documents["str"].contents[0][0].parsed, parsed)

        # int

        parsed = {
            "sphinx":  5,
        }

        instance.document("stuffies", "thingins", parsed)

        self.assertEqual(instance.documents["index"].contents[5][0].module, "stuffies")
        self.assertEqual(instance.documents["index"].contents[5][0].kind, "thingins")
        self.assertEqual(instance.documents["index"].contents[5][0].parsed, parsed)

        # full

        parsed = {
            "sphinx": {
                "path": "full",
                "order": 10
            }
        }

        instance.document("stuffins", "thingies", parsed)

        self.assertEqual(instance.documents["full"].path, "docs/source/full.rst")
        self.assertEqual(instance.documents["full"].contents[10][0].module, "stuffins")
        self.assertEqual(instance.documents["full"].contents[10][0].kind, "thingies")
        self.assertEqual(instance.documents["full"].contents[10][0].parsed, parsed)

    def test_read(self):

        instance = sphinxter.Sphinxter(example)

        instance.read()

        self.assertEqual(instance.documents["index"].contents[0][0].module, "test.example")
        self.assertEqual(instance.documents["index"].contents[0][0].kind, "module")
        self.assertEqual(instance.documents["index"].contents[0][0].parsed, TestReader.MODULE)

        self.assertEqual(instance.documents["index"].contents[0][1].module, "test.example")
        self.assertEqual(instance.documents["index"].contents[0][1].kind, "function")
        self.assertEqual(instance.documents["index"].contents[0][1].parsed, TestReader.FUNCTION)

        self.assertEqual(instance.documents["index"].contents[0][2].module, "test.example")
        self.assertEqual(instance.documents["index"].contents[0][2].kind, "class")
        self.assertEqual(instance.documents["index"].contents[0][2].parsed, TestReader.BASIC_CLASS)

        self.assertEqual(instance.documents["index"].contents[0][3].module, "test.example")
        self.assertEqual(instance.documents["index"].contents[0][3].kind, "class")
        self.assertEqual(instance.documents["index"].contents[0][3].parsed, TestReader.COMPLEX_CLASS)

        self.assertEqual(len(instance.documents["index"].contents), 1)
        self.assertEqual(len(instance.documents["index"].contents[0]), 4)

    @unittest.mock.patch('sphinxter.open', new_callable=unittest.mock.mock_open)
    def test_write(self, mock_open):

        instance = sphinxter.Sphinxter(example)

        instance.read()
        instance.write()

        mock_open.assert_called_once_with("docs/source/index.rst", "w", encoding="utf-8")

        self.assertEqual("\n" + "".join([call.args[0] for call in mock_open.return_value.write.mock_calls]), TestWriter.EXAMPLE)

    @unittest.mock.patch('sphinxter.open', new_callable=unittest.mock.mock_open)
    def test_process(self, mock_open):

        instance = sphinxter.Sphinxter(example)

        instance.process()

        self.assertEqual("\n" + "".join([call.args[0] for call in mock_open.return_value.write.mock_calls]), TestWriter.EXAMPLE)
