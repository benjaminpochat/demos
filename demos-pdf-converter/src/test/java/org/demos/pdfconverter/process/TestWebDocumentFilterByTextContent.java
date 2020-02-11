package org.demos.pdfconverter.process;

import org.demos.pdfconverter.model.WebDocument;
import org.junit.jupiter.api.Test;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

import static org.assertj.core.api.Assertions.assertThat;

public class TestWebDocumentFilterByTextContent {
    @Test
    public void test_should_return_true_when_a_document_converted_as_text_is_not_empty() throws IOException {
        // given
        String path = this.getClass().getResource("/org/demos/pdfconverter/TestWebDocumentFilterBySize_file_small_enough.pdf").getPath();
        FileInputStream inputStream = new FileInputStream(path);
        var webDocument = new WebDocument();
        webDocument.setPdfContent(inputStream.readAllBytes());
        var converter = new PdfConverter();
        webDocument = converter.convert(webDocument);
        var filter = new WebDocumentFilterByTextContent();

        // when
        boolean isSmallEnough = filter.test(webDocument);

        // then
        assertThat(isSmallEnough).isTrue();
    }

    @Test
    public void test_should_return_false_when_a_document_converted_as_text_is_empty() {
        // given
        var webDocument = new WebDocument();
        var filter = new WebDocumentFilterByTextContent();

        // when
        boolean isSmallEnough = filter.test(webDocument);

        // then
        assertThat(isSmallEnough).isFalse();
    }
}
