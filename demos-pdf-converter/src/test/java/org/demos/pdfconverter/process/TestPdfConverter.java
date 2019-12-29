package org.demos.pdfconverter.process;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.demos.pdfconverter.model.WebDocument;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static org.assertj.core.api.Assertions.assertThat;

public class TestPdfConverter {
    @Test
    public void convert_should_convert_a_simple_pdf() throws IOException {
        // given
        String path = this.getClass().getResource("/org/demos/pdfconverter/TestPdfConverter_cas1.pdf").getPath();
        var webDocument = new WebDocument();
        webDocument.setUrl("file://" + path);
        var converter = new PdfConverter();

        // when
        webDocument = converter.convert(webDocument);

        // then
        Path expectedPdfContentFile = Paths.get(this.getClass().getResource("/org/demos/pdfconverter/TestPdfConverter_cas1.txt").getPath());
        assertThat(webDocument.getTextContent()).isEqualTo(new String(Files.readAllBytes(expectedPdfContentFile)));
        assertThat(webDocument.getUrl()).isEqualTo("file://" + path);
    }

    @Test
    public void convert_sould_not_throw_an_exception_if_an_out_of_memory_error_occurs() {
        // given
        String path = this.getClass().getResource("/org/demos/pdfconverter/TestPdfConverter_cas1.pdf").getPath();
        var webDocument = new WebDocument();
        webDocument.setUrl("file://" + path);
        var converter = new PdfConverter(){
            @Override
            PDDocument getPDDocument(InputStream inputStream) {
                throw new OutOfMemoryError();
            }
        };

        // when
        webDocument = converter.convert(webDocument);

        // then
        assertThat(webDocument).isNotNull();
        assertThat(webDocument.getTextContent()).isNull();

    }
}
