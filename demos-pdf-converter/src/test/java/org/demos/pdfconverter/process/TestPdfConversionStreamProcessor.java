package org.demos.pdfconverter.process;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsConfig;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.Properties;

public class TestPdfConversionStreamProcessor {

    @Test
    public void new_PdfConversionStreamProcessor_should_contains_hard_coded_kafka_properties_if_no_arguments_is_given(){
        // given
        String[] arguments = new String[]{};

        // when
        PdfConversionStreamProcessor pdfConversionStreamProcessor = new PdfConversionStreamProcessor(arguments);

        // then
        Properties expectedKafkaProperties = new Properties();
        expectedKafkaProperties.put(StreamsConfig.APPLICATION_ID_CONFIG, "pdf-converter");
        expectedKafkaProperties.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        expectedKafkaProperties.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        expectedKafkaProperties.setProperty(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        Assertions.assertThat(pdfConversionStreamProcessor.getKafkaProperties()).containsAllEntriesOf(expectedKafkaProperties);
    }


    @Test
    public void new_PdfConversionStreamProcessor_should_read_kafka_arguments_correctly(){
        // given
        String[] arguments = new String[]{"kafka.bootstrap.servers=my-kafka-server:9999", "kafka.any.kafka.porperty=AnyValue"};

        // when
        PdfConversionStreamProcessor pdfConversionStreamProcessor = new PdfConversionStreamProcessor(arguments);

        // then
        Properties expectedKafkaProperties = new Properties();
        expectedKafkaProperties.setProperty("bootstrap.servers", "my-kafka-server:9999");
        expectedKafkaProperties.setProperty("any.kafka.porperty", "AnyValue");
        Assertions.assertThat(pdfConversionStreamProcessor.getKafkaProperties()).containsAllEntriesOf(expectedKafkaProperties);
    }

    @Test
    public void new_PdfConversionStreamProcessor_should_never_read_application_id_in_arguments(){
        // given
        String[] arguments = new String[]{"kafka.application.id=toto"};

        // when
        PdfConversionStreamProcessor pdfConversionStreamProcessor = new PdfConversionStreamProcessor(arguments);

        // then
        Properties expectedKafkaProperties = new Properties();
        expectedKafkaProperties.setProperty("application.id", "pdf-converter");
        Assertions.assertThat(pdfConversionStreamProcessor.getKafkaProperties()).containsAllEntriesOf(expectedKafkaProperties);
    }


    @Test
    public void new_PdfConversionStreamProcessor_should_set_a_default_value_for_kafka_bootstrap_servers(){
        // given
        String[] arguments = new String[]{};

        // when
        PdfConversionStreamProcessor pdfConversionStreamProcessor = new PdfConversionStreamProcessor(arguments);

        // then
        Properties expectedKafkaProperties = new Properties();
        expectedKafkaProperties.setProperty("bootstrap.servers", "localhost:9092");
        Assertions.assertThat(pdfConversionStreamProcessor.getKafkaProperties()).containsAllEntriesOf(expectedKafkaProperties);
    }

    @Test
    public void new_PdfConversionStreamProcessor_should_read_conversion_task_timeout_correctly(){
        // given
        String[] arguments = new String[]{"conversion.task.timeout=10"};

        // when
        PdfConversionStreamProcessor pdfConversionStreamProcessor = new PdfConversionStreamProcessor(arguments);

        // then
        Assertions.assertThat(pdfConversionStreamProcessor.getConversionTaskTimeout()).isEqualTo(10);
    }

    @Test
    public void new_PdfConversionStreamProcessor_should_set_a_default_value_for_conversion_task_timeout(){
        // given
        String[] arguments = new String[]{};

        // when
        PdfConversionStreamProcessor pdfConversionStreamProcessor = new PdfConversionStreamProcessor(arguments);

        // then
        Assertions.assertThat(pdfConversionStreamProcessor.getConversionTaskTimeout()).isEqualTo(240000);
    }
}
