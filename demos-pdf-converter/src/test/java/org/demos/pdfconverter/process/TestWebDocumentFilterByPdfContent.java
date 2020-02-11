package org.demos.pdfconverter.process;

import org.assertj.core.api.Assertions;
import org.demos.pdfconverter.model.WebDocument;
import org.junit.jupiter.api.Test;

import java.io.FileInputStream;
import java.io.IOException;

public class TestWebDocumentFilterByPdfContent {
    @Test
    public void test_should_return_false_if_pdf_content_is_null(){
        // given
        WebDocumentFilterByPdfContent filter = new WebDocumentFilterByPdfContent();
        WebDocument webDocument = new WebDocument();

        // when
        boolean result = filter.test(webDocument);

        // then
        Assertions.assertThat(result).isFalse();
    }

    @Test
    public void test_should_return_false_if_pdf_content_is_empty(){
        // given
        WebDocumentFilterByPdfContent filter = new WebDocumentFilterByPdfContent();
        WebDocument webDocument = new WebDocument();
        webDocument.setPdfContent(new byte[0]);

        // when
        boolean result = filter.test(webDocument);

        // then
        Assertions.assertThat(result).isFalse();
    }


    @Test
    public void test_should_return_true_if_pdf_content_is_not_empty() throws IOException {
        // given
        WebDocumentFilterByPdfContent filter = new WebDocumentFilterByPdfContent();
        String path = this.getClass().getResource("/org/demos/pdfconverter/TestWebDocumentFilterBySize_file_small_enough.pdf").getPath();
        FileInputStream inputStream = new FileInputStream(path);
        var webDocument = new WebDocument();
        webDocument.setPdfContent(inputStream.readAllBytes());

        // when
        boolean result = filter.test(webDocument);

        // then
        Assertions.assertThat(result).isTrue();
    }
}
