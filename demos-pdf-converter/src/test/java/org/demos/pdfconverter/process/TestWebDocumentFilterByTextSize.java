package org.demos.pdfconverter.process;

import org.demos.pdfconverter.model.WebDocument;
import org.junit.jupiter.api.Test;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

import static org.assertj.core.api.Assertions.assertThat;

public class TestWebDocumentFilterByTextSize {

    @Test
    public void test_should_return_false_when_a_document_converted_as_text_is_too_big() throws IOException {
        // given
        String path = this.getClass().getResource("/org/demos/pdfconverter/TestWebDocumentFilterBySize_file_too_big.pdf").getPath();
        FileInputStream inputStream = new FileInputStream(path);
        var webDocument = new WebDocument();
        webDocument.setPdfContent(inputStream.readAllBytes());
        var converter = new PdfConverter();
        webDocument = converter.convert(webDocument);
        WebDocumentFilterByTextSize filter = new WebDocumentFilterByTextSize();

        // when
        boolean isSmallEnough = filter.test(webDocument);

        // then
        assertThat(isSmallEnough).isFalse();
    }

    @Test
    public void test_should_return_false_when_a_document_converted_as_text_is_small_enough() throws IOException {
        // given
        String path = this.getClass().getResource("/org/demos/pdfconverter/TestWebDocumentFilterBySize_file_small_enough.pdf").getPath();
        FileInputStream inputStream = new FileInputStream(path);
        var webDocument = new WebDocument();
        webDocument.setPdfContent(inputStream.readAllBytes());
        var converter = new PdfConverter();
        webDocument = converter.convert(webDocument);
        WebDocumentFilterByTextSize filter = new WebDocumentFilterByTextSize();

        // when
        boolean isSmallEnough = filter.test(webDocument);

        // then
        assertThat(isSmallEnough).isTrue();
    }
}
