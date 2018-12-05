import unittest
import os
import re
from src.main.python.process.data_preparation.pdf_converter.pdf_converter import PdfConverter


class TestPdfConverter(unittest.TestCase):
    def test_convert_simple_pdf_ok(self):
        # given
        pdf_converter = PdfConverter(timeout=60)
        simple_pdf_file_path = os.path.join(os.path.dirname(__file__),
                                            '../../../../resources/data_preparation/pdf_converter/simple.pdf')
        simple_pdf_file = open(simple_pdf_file_path, 'rb')
        pdf_bytes = simple_pdf_file.read()
        simple_pdf_file.close()

        # when
        pdf_text_content = pdf_converter.convert(pdf_bytes)

        # then
        # TODO : the simple pdf, file generated with LibreOffice, is converted with carriage returns at the end.
        # For this reason we use regex in the assertion.
        # It would be better if the conversion result contained only "Hello world !".
        self.assertTrue(re.match('^Hello world !\s*$', pdf_text_content))

    def test_convert_complex_pdf_ok(self):
        # given
        timeout_in_seconds = 1
        pdf_converter = PdfConverter(timeout=timeout_in_seconds)
        complex_pdf_file_path = os.path.join(os.path.dirname(__file__),
                                             '../../../../resources/data_preparation/pdf_converter/complex.pdf')
        complex_pdf_file = open(complex_pdf_file_path, 'rb')
        pdf_bytes = complex_pdf_file.read()
        complex_pdf_file.close()

        # when
        pdf_text_content = pdf_converter.convert(pdf_bytes)

        # then
        self.assertEqual('', pdf_text_content)


if __name__ == '__main__':
    unittest.main()
