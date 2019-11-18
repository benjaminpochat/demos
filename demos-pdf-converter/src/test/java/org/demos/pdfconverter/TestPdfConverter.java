package org.demos.pdfconverter;

import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;

import java.io.*;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class TestPdfConverter {
    @Test
    public void convertPdfToText_should_convert_a_simple_pdf() throws IOException {
        // given
        String path = this.getClass().getResource("/org/demos/pdfconverter/TestPdfConverter_cas1.pdf").getPath();
        PdfConverter converter = new PdfConverter();

        // when
        String pdfContent = converter.converts("file://" + path);

        // then
        Path expectedPdfContentFile = Paths.get(this.getClass().getResource("/org/demos/pdfconverter/TestPdfConverter_cas1.txt").getPath());
        Assertions.assertThat(pdfContent).isEqualTo(new String(Files.readAllBytes(expectedPdfContentFile)));
    }
}
