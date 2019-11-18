package org.demos.pdfconverter;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;

import java.util.Properties;

public class PdfConversionStreamProcessor {
    public static void main(String[] args){
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "pdf-converter");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        StreamsBuilder builder = new StreamsBuilder();
        PdfConverter converter = new PdfConverter();
        KStream<String, String> pdfUrls = builder.stream("UnclassifiedPdfUrl");
        pdfUrls.mapValues(converter::converts)
                .filter((key, value) -> value != null)
                .to("UnclassifiedPdfContent");

        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        streams.start();
    }
}
