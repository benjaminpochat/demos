package org.demos.pdfconverter.process;

import org.demos.core.domains.webdocument.WebDocument;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static org.assertj.core.api.Assertions.assertThat;

public class TestPdfConverter {
    @Test
    public void convertPdfToText_should_convert_a_simple_pdf() throws IOException {
        // given
        String path = this.getClass().getResource("/org/demos/pdfconverter/TestPdfConverter_cas1.pdf").getPath();
        WebDocument webDocument = new WebDocument();
        webDocument.setUrl("file://" + path);
        PdfConverter converter = new PdfConverter();

        // when
        webDocument = converter.convert(webDocument);

        // then
        Path expectedPdfContentFile = Paths.get(this.getClass().getResource("/org/demos/pdfconverter/TestPdfConverter_cas1.txt").getPath());
        assertThat(webDocument.getTextContent()).isEqualTo(new String(Files.readAllBytes(expectedPdfContentFile)));
        assertThat(webDocument.getUrl()).isEqualTo("file://" + path);
    }
}
