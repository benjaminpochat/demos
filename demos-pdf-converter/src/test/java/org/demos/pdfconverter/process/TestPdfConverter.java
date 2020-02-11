package org.demos.pdfconverter.process;

import org.demos.pdfconverter.model.WebDocument;
import org.demos.pdfconverter.process.PdfConverter.ConversionTask;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.mockito.stubbing.Answer;

import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.concurrent.TimeoutException;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.*;

public class TestPdfConverter {
    @Test
    public void convert_should_convert_a_simple_pdf() throws IOException {
        // given
        String path = this.getClass().getResource("/org/demos/pdfconverter/TestPdfConverter_cas1.pdf").getPath();
        FileInputStream inputStream = new FileInputStream(path);
        var webDocument = new WebDocument();
        webDocument.setPdfContent(inputStream.readAllBytes());
        var converter = new PdfConverter();

        // when
        webDocument = converter.convert(webDocument);

        // then
        Path expectedPdfContentFile = Paths.get(this.getClass().getResource("/org/demos/pdfconverter/TestPdfConverter_cas1.txt").getPath());
        assertThat(webDocument.getTextContent()).isEqualTo(new String(Files.readAllBytes(expectedPdfContentFile)));
    }

    @Test
    public void executeConversionTaskInWithinTimeoutDuration_should_throw_an_exception_if_the_timeout_is_reached() {
        // given
        ConversionTask conversionTask = mock(ConversionTask.class);
        Mockito.doAnswer((Answer<Void>) invocation -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return null;
        }).when(conversionTask).run();
        PdfConverter converter = spy(PdfConverter.class);
        when(converter.getConversionTask(any(WebDocument.class))).thenReturn(conversionTask);
        when(converter.getTimeout()).thenReturn(500);

        // when / then
        assertThrows(TimeoutException.class, () -> converter.executeConversionTaskInWithinTimeoutDuration(new WebDocument()));
    }
}
