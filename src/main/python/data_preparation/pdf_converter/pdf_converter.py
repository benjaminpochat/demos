import os
import sys
import logging

from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from logging import StreamHandler


class PdfConverter:
    """
    A class for converting a bunch of pdf files into text files.
    """

    def __init__(self):
        self._init_logger()

    def _init_logger(self):
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.INFO)
        log_handler = StreamHandler()
        log_handler.setLevel(logging.INFO)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self._logger.addHandler(log_handler)

    def convert(self, file_name_path : str, pages=None):
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)
        output = StringIO()
        manager = PDFResourceManager()
        pdf_to_text_converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, pdf_to_text_converter)
        infile = open(file_name_path, 'rb')
        try:
            page_number = 1
            for page in PDFPage.get_pages(infile, pagenums):
                self._logger.info('Interprating page %s' % page_number)
                interpreter.process_page(page)
                page_number = page_number + 1
        except:
            e = sys.exc_info()[0]
            self._logger.warning("Error: %s" % e)
        infile.close()
        pdf_to_text_converter.close()
        text = output.getvalue()
        output.close()
        return text

    def convert_directory_content(self, input_directory_path : str, output_directory_path : str):
        for input_file_name in os.listdir(input_directory_path):
            input_file_path = input_directory_path + "/" + input_file_name
            output_file_path = output_directory_path + "/" + input_file_name + ".txt"
            self.convert_file(input_file_path, output_file_path)

    def convert_file(self, input_file_path : str, output_file_path : str):
        self._logger.info("Converting " + input_file_path + " to " + output_file_path)
        output_file = open(output_file_path, "w")
        output_file.write(self.convert(input_file_path))

    def convert_sub_directories(self, input_directory_path : str, output_directoy_path : str):
        """
        Iterate over all of subdirectories of the given input_directory_path,
        create a subdirectory with the same name into the given output_directoy_path,
        and converts all pdf files present in the input subdirectories as text files in the output subdirectories.
        :param input_directory_path: the path of the input directory
        :param output_directoy_path: the path of the output directory
        :return: nothing
        """
        for input_subdir_name in os.listdir(input_directory_path):
            input_subdir_path = input_directory_path + "/" + input_subdir_name
            output_subdir_path = output_directoy_path + "/" + input_subdir_name
            os.makedirs(output_subdir_path, exist_ok=True)
            self.convert_directory_content(input_subdir_path, output_subdir_path)


if __name__ == '__main__':
    converter = PdfConverter()
    converter.convert_sub_directories("./data/pdf", "./data/text")

