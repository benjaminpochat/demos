package org.demos.pdfconverter.process;

import org.demos.pdfconverter.model.WebDocument;
import org.demos.pdfconverter.process.PdfDownloader.DownloadTask;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

public class TestPdfDownloader {
    @Test
    public void download_should_fill_web_document_pdf_content() throws PdfDownloader.PdfFileTooBigException, PdfDownloader.PdfUrlNotValidException, NoSuchAlgorithmException, IOException, KeyManagementException {
        // given
        var webDocument = new WebDocument();
        String path = webDocument.getClass().getResource("/org/demos/pdfconverter/TestPdfConverter_cas1.pdf").getPath();
        webDocument.setUrl("file://" + path);
        PdfDownloader downloader = new PdfDownloader(100000);

        // when
        downloader.download(webDocument);

        // then
        assertThat(webDocument.getPdfContent()).isNotNull();
        assertThat(webDocument.getPdfContent().length).isLessThan(100000);
        assertThat(webDocument.getPdfContent().length).isBetween(1, 100000);
    }

    @Test
    public void download_should_throw_an_exception_if_the_file_is_too_big() {
        // given
        var webDocument = new WebDocument();
        String path = webDocument.getClass().getResource("/org/demos/pdfconverter/TestPdfConverter_cas1.pdf").getPath();
        webDocument.setUrl("file://" + path);
        DownloadTask downloadTask = new DownloadTask(webDocument, 100);

        // when / then
        assertThatThrownBy(downloadTask::download).isInstanceOf(PdfDownloader.PdfFileTooBigException.class);
    }

    @Test
    public void download_should_throw_an_exception_if_the_url_is_invalid()  {
        // given
        var webDocument = new WebDocument();
        String path = webDocument.getClass().getResource("/org/demos/pdfconverter/TestPdfConverter_cas1.pdf").getPath();
        webDocument.setUrl("file://" + path + "x");
        DownloadTask downloadTask = new DownloadTask(webDocument, 100);

        // when / then
        assertThatThrownBy(downloadTask::download).isInstanceOf(PdfDownloader.PdfUrlNotValidException.class);
    }

    @Test
    public void download_should_fill_web_document_pdf_content_with_http_url() throws PdfDownloader.PdfUrlNotValidException, PdfDownloader.PdfFileTooBigException, NoSuchAlgorithmException, IOException, KeyManagementException {
        // given
        var webDocument = new WebDocument();
        webDocument.setUrl("https://raw.githubusercontent.com/benjaminpochat/demos/master/README.md");
        PdfDownloader downloader = new PdfDownloader(10000);

        // when
        downloader.download(webDocument);

        // then
        assertThat(webDocument.getPdfContent()).isNotNull();
        assertThat(webDocument.getPdfContent().length).isLessThan(100000);
        assertThat(webDocument.getPdfContent().length).isBetween(1, 100000);
    }
}
