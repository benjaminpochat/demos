package org.demos.pdfconverter.process;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Produced;
import org.demos.pdfconverter.model.WebDocument;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Properties;

public class PdfConversionStreamProcessor {

    private static final Logger LOGGER = LoggerFactory.getLogger(PdfConversionStreamProcessor.class);

    private static final String INPUT_TOPIC_NAME = "UnclassifiedPdfUrl";

    private static final String OUTPUT_TOPIC_NAME = "UnclassifiedPdfContent";

    public static final String DEFAULT_SERVERS_CONFIG = "localhost:9092";

    private WebDocumentFilterByContent filterByContent = new WebDocumentFilterByContent();

    private WebDocumentFilterBySize filterBySize = new WebDocumentFilterBySize(WebDocumentFilterBySize.DEFAULT_MAXIMUM_TEXT_CONTENT_SIZE);

    private WebDocumentIdGenerator idGenerator = new WebDocumentIdGenerator();

    private final Properties properties = new Properties();

    private Serde<WebDocument> webDocumentSerde = Serdes.serdeFrom(new UnclassifiedWebDocumentSerializer(), new UnclassifierWebDocumentDeserializer());

    private PdfConverter converter = new PdfConverter();

    public PdfConversionStreamProcessor() {
        this(DEFAULT_SERVERS_CONFIG);
    }

    public PdfConversionStreamProcessor(String serversConfig){
        properties.put(StreamsConfig.APPLICATION_ID_CONFIG, "pdf-converter");
        properties.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, serversConfig);
        properties.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        properties.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
    }

    public static void main(String[] args) {
        new PdfConversionStreamProcessor().process();
    }

    private void process(){
        StreamsBuilder builder = new StreamsBuilder();
        KStream<String, WebDocument> pdfUrlStream = builder.stream(INPUT_TOPIC_NAME, Consumed.with(Serdes.String(), webDocumentSerde));
        KStream<String, WebDocument> webDocumentStream = pdfUrlStream.mapValues(converter::convert)
                .filter((url, webDocument) -> filterByContent.test(webDocument))
                .filter((url, webDocument) -> filterBySize.test(webDocument))
                .mapValues(webDocument -> idGenerator.generateId(webDocument));
        webDocumentStream.to(OUTPUT_TOPIC_NAME, Produced.with(Serdes.String(), webDocumentSerde));
        KafkaStreams streams = new KafkaStreams(builder.build(), properties);
        streams.start();
    }
}
