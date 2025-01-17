import unittest

from parse_markdown import block_to_block_type


class TestBlockType(unittest.TestCase):
    def test_heading(self):
        heading1 = "### sdfasdf*seikdjlsdf./:?"
        heading2 = "## sdfasdf*seijlsdf./:?"
        noheading1 = "####### sdfasdf*seijlsdf./:?"
        noheading2 = "###asdfsdf"
        noheading3 = "sflkjasf"
        self.assertEqual(block_to_block_type(heading1), "heading")
        self.assertEqual(block_to_block_type(heading2), "heading")

        self.assertEqual(block_to_block_type(noheading1), "paragraph")
        self.assertEqual(block_to_block_type(noheading2), "paragraph")
        self.assertEqual(block_to_block_type(noheading3), "paragraph")

    def test_code(self):
        code1 = """```sdfsdfsdfsdfsdfsdf

        ```"""
        nocode = "``lkjasf```"
        self.assertEqual(block_to_block_type(code1), "code")
        self.assertEqual(block_to_block_type(nocode), "paragraph")

    def test_quote(self):
        quote = """>asdf
        >ssgefeflkj
        >jlkjdfefil"""
        noquote = "s>ffief"
        self.assertEqual(block_to_block_type(quote), "quote")
        self.assertEqual(block_to_block_type(noquote), "paragraph")

    def test_ulist(self):
        list = """* sdfsdfsdfsdf
        - sdfsdfsdfsdf
        * sdfsdfsdf"""
        nolist = """*sdfsdfsdf
        -sdfsdfsd"""
        self.assertEqual(block_to_block_type(list), "unordered_list")
        self.assertEqual(block_to_block_type(nolist), "paragraph")
