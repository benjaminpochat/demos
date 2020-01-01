package org.demos.pdfconverter.process;

import org.assertj.core.api.Assertions;
import org.demos.pdfconverter.model.WebDocument;
import org.junit.jupiter.api.Test;

public class TestWebDocumentIdGenerator {

    @Test
    public void generateId_should_not_return_null(){
        // given
        WebDocument webDocument = new WebDocument();
        webDocument.setTextContent("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.");
        var webDocumentIdGenerator = new WebDocumentIdGenerator();

        // when
        webDocumentIdGenerator.generateId(webDocument);

        // then
        Assertions.assertThat(webDocument.getId()).isNotEmpty();
    }
}
