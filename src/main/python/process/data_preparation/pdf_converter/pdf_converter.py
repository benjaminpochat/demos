import signal

from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from tempfile import SpooledTemporaryFile
from src.main.python.commons.loggable import Loggable


class PdfConverter(Loggable):
    def __init__(self, timeout: int = 60):
        super().__init__()
        self._timeout = timeout

    def convert(self, pdf_bytes):
        temporary_pdf_file = SpooledTemporaryFile()
        temporary_pdf_file.write(pdf_bytes)
        manager = PDFResourceManager()
        output = StringIO()
        pdf_to_text_converter = TextConverter(manager, output, 'utf-8', laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, pdf_to_text_converter)

        def timeout_handler(signum, frame):
            raise Exception("timeout reached (" + str(self._timeout) + 's)')

        try:
            page_number = 1
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self._timeout )
            for page in PDFPage.get_pages(temporary_pdf_file):
                self.log_info('Interprating page %s' % page_number)
                interpreter.process_page(page)
                page_number = page_number + 1
        except Exception as e:
            self.log_error("Exception raised : %s" % e)
        pdf_to_text_converter.close()
        text = output.getvalue()
        output.close()
        return text
