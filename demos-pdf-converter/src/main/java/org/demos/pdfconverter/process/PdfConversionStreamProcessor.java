package org.demos.pdfconverter.process;

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

import java.util.Map;
import java.util.Properties;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class PdfConversionStreamProcessor {

    private static final Logger LOGGER = LoggerFactory.getLogger(PdfConversionStreamProcessor.class);

    private static final String INPUT_TOPIC_NAME = "UnclassifiedPdfUrl";

    private static final String OUTPUT_TOPIC_NAME = "UnclassifiedPdfContent";

    private static final String DEFAULT_SERVERS_CONFIG = "localhost:9092";

    private static final String KAFKA_ARGUMENTS_PREFIX = "kafka.";

    private static final String KAFKA_APPLICATION_ID = "pdf-converter";

    private static final String CONVERSION_TASK_TIMEOUT_KEY = "conversion.task.timeout";

    private static final String MAXIMUM_TEXT_CONTENT_SIZE_KEY = "maximum.text.content.size";

    private WebDocumentFilterByContent filterByContent;

    private WebDocumentFilterBySize filterBySize;

    private WebDocumentIdGenerator idGenerator;

    private Properties kafkaProperties;

    private int conversionTaskTimeout;

    private int maximumTextContentSize;

    private Serde<WebDocument> webDocumentSerde = Serdes.serdeFrom(new UnclassifiedWebDocumentSerializer(), new UnclassifierWebDocumentDeserializer());

    private PdfConverter converter;

    public Properties getKafkaProperties() {
        return kafkaProperties;
    }

    public int getConversionTaskTimeout() {
        return conversionTaskTimeout;
    }

    public PdfConversionStreamProcessor(String[] arguments){
        setKafkaProperties(arguments);
        parsePdfConverterArguments(arguments);
        filterBySize = new WebDocumentFilterBySize(maximumTextContentSize);
        filterByContent = new WebDocumentFilterByContent();
        idGenerator = new WebDocumentIdGenerator();
        if(conversionTaskTimeout > 0) {
            converter = new PdfConverter(conversionTaskTimeout);
        } else {
            converter = new PdfConverter();
        }
    }

    private void setKafkaProperties(String[] arguments) {
        kafkaProperties = new Properties();
        parseKafkaArguments(arguments);
        setHardCodedKafkaArguments();
    }

    private void parsePdfConverterArguments(String[] arguments) {
        Map<String, String> pdfConverterPropertiesMap = Stream.of(arguments)
                .filter(argument -> !argument.startsWith(KAFKA_ARGUMENTS_PREFIX))
                .collect(Collectors.toMap(
                        argument -> argument.split("=")[0],
                        argument -> argument.split("=")[1]
                ));
        LOGGER.info("The PdfConvert arguments are :");
        pdfConverterPropertiesMap.entrySet().forEach(entry -> LOGGER.info(entry.getKey() + " = " + entry.getValue()));
        conversionTaskTimeout = Integer.valueOf(pdfConverterPropertiesMap.getOrDefault(CONVERSION_TASK_TIMEOUT_KEY, "-1"));
        maximumTextContentSize = Integer.valueOf(pdfConverterPropertiesMap.getOrDefault(MAXIMUM_TEXT_CONTENT_SIZE_KEY, "-1"));
    }

    private void parseKafkaArguments(String[] arguments) {
        Map<String, String> kafkaPropertiesMap = Stream.of(arguments)
                .filter(argument -> argument.startsWith(KAFKA_ARGUMENTS_PREFIX))
                .collect(Collectors.toMap(
                        argument -> argument.split("=")[0].substring(KAFKA_ARGUMENTS_PREFIX.length()),
                        argument -> argument.split("=")[1]
                ));
        kafkaProperties.putAll(kafkaPropertiesMap);
    }

    private void setHardCodedKafkaArguments() {
        if(!kafkaProperties.containsKey(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG)){
            kafkaProperties.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, DEFAULT_SERVERS_CONFIG);
        }
        kafkaProperties.put(StreamsConfig.APPLICATION_ID_CONFIG, KAFKA_APPLICATION_ID);
        kafkaProperties.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        kafkaProperties.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        LOGGER.info("The kafka properties are :");
        kafkaProperties.entrySet().forEach(entry -> LOGGER.info(entry.getKey() + " = " + entry.getValue()));

    }

    public static void main(String[] args) {
        new PdfConversionStreamProcessor(args).process();
    }

    private void process(){
        StreamsBuilder builder = new StreamsBuilder();
        KStream<String, WebDocument> pdfUrlStream = builder.stream(INPUT_TOPIC_NAME, Consumed.with(Serdes.String(), webDocumentSerde));
        KStream<String, WebDocument> webDocumentStream = pdfUrlStream.mapValues(converter::convert)
                .filter((url, webDocument) -> filterByContent.test(webDocument))
                .filter((url, webDocument) -> filterBySize.test(webDocument))
                .mapValues(webDocument -> idGenerator.generateId(webDocument));
        webDocumentStream.to(OUTPUT_TOPIC_NAME, Produced.with(Serdes.String(), webDocumentSerde));
        KafkaStreams streams = new KafkaStreams(builder.build(), kafkaProperties);
        streams.start();
    }
}
