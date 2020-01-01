package org.demos.pdfconverter.process;

import org.demos.pdfconverter.model.WebDocument;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

public class TestWebDocumentFilterBySize {

    @Test
    public void test_should_return_false_for_a_document_too_big() {
        // given
        String path = this.getClass().getResource("/org/demos/pdfconverter/TestWebDocumentFilterBySize_file_too_big.pdf").getPath();
        var webDocument = new WebDocument();
        webDocument.setUrl("file://" + path);
        var converter = new PdfConverter();
        webDocument = converter.convert(webDocument);
        WebDocumentFilterBySize filter = new WebDocumentFilterBySize();

        // when
        boolean isSmallEnough = filter.test(webDocument);

        // then
        assertThat(isSmallEnough).isFalse();
    }

    @Test
    public void test_should_return_false_for_a_document_small_enough() {
        // given
        String path = this.getClass().getResource("/org/demos/pdfconverter/TestWebDocumentFilterBySize_file_small_enough.pdf").getPath();
        var webDocument = new WebDocument();
        webDocument.setUrl("file://" + path);
        var converter = new PdfConverter();
        webDocument = converter.convert(webDocument);
        WebDocumentFilterBySize filter = new WebDocumentFilterBySize();

        // when
        boolean isSmallEnough = filter.test(webDocument);

        // then
        assertThat(isSmallEnough).isTrue();
    }
}
