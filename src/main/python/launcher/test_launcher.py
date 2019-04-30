import urllib.request

from src.main.python.launcher.launcher import Launcher, ManualPage


class TestLauncher(Launcher):

    def __init__(self, args: list):
        super().__init__(args)

    def get_manual_page(self):
        return TestManualPage()

    def start_process(self):

        from src.main.python.process.archiving.pdf_classifier import LocalGovernmentPdfClassifier
        from src.main.python.process.pdf_converter.pdf_converter import PdfConverter

        url = self.args[0]
        pdf_content = urllib.request.urlopen(url).read()
        text_content = PdfConverter(timeout=300).convert(pdf_content)
        classification = LocalGovernmentPdfClassifier().classify(text_content)
        print(classification.class_prediction)
        if classification.isOfficialCouncilReport():
            print('Yep : the PDF at ' + url + ' has been classified as an official city council report')
        else:
            print('Nope : the PDF at ' + url + ' has not been classified as an official city council report')


class TestManualPage(ManualPage):

    def get_usage(self):
        return 'Usage : demos test http://an/url/to/a/file.pdf'

    def get_title(self):
        return 'Welcome in Demos test manual page !'

    def get_description(self):
        return 'Demos test module allow the user to run the classification model to evaluate its relevance'
