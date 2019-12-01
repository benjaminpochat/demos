package org.demos.pdfconverter.process;

import org.apache.pdfbox.cos.COSDocument;
import org.apache.pdfbox.io.RandomAccessBuffer;
import org.apache.pdfbox.io.RandomAccessRead;
import org.apache.pdfbox.pdfparser.PDFParser;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.demos.pdfconverter.model.WebDocument;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;

public class PdfConverter {

    static Logger LOGGER = LoggerFactory.getLogger(PdfConverter.class);

    public WebDocument convert(WebDocument webDocument) {
        LOGGER.info("url " + webDocument.getUrl() + " is getting converted...");
        String parsedText = null;
        PDDocument pdDoc = null;
        try{
            initSSLSocketFactory();
            URL url = new URL(webDocument.getUrl());
            URLConnection conn = url.openConnection();
            InputStream in = conn.getInputStream();
            RandomAccessRead randomAccessRead = new RandomAccessBuffer(in);
            PDFParser parser = new PDFParser(randomAccessRead);
            parser.parse();
            COSDocument cosDoc = parser.getDocument();
            PDFTextStripper pdfStripper = new PDFTextStripper();
            pdDoc = new PDDocument(cosDoc);
            parsedText = pdfStripper.getText(pdDoc);
            pdDoc.close();
        } catch (IOException | NoSuchAlgorithmException | KeyManagementException e){
            LOGGER.error("An error occurs while converting " + webDocument.getUrl() + " into text.", e);
        }
        webDocument.setTextContent(parsedText);
        return webDocument;
    }

    private void initSSLSocketFactory() throws NoSuchAlgorithmException, KeyManagementException {
        TrustManager[] trustAllCerts = getTrustManagers();
        SSLContext sslContext = SSLContext.getInstance("SSL");
        sslContext.init(null, trustAllCerts, new java.security.SecureRandom());
        HttpsURLConnection.setDefaultSSLSocketFactory(sslContext.getSocketFactory());
    }

    private TrustManager[] getTrustManagers() {
        return new TrustManager[]{
            new X509TrustManager() {
                public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                    return null;
                }
                public void checkClientTrusted(
                        java.security.cert.X509Certificate[] certs, String authType) {
                }
                public void checkServerTrusted(
                        java.security.cert.X509Certificate[] certs, String authType) {
                }
            }
        };
    }
}
