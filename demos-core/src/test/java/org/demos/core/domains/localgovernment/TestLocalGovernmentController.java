package org.demos.core.domains.localgovernment;

import org.demos.core.domains.webdocument.WebDocument;
import org.demos.model.domains.localgovernment.LocalGovernmentType;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.jdbc.Sql;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@RunWith(SpringRunner.class)
@SpringBootTest
@Transactional
@Sql({"/org/demos/core/domains/localgovernment/TestLocalGovernmentController.sql"})
public class TestLocalGovernmentController {

    @Autowired
    LocalGovernmentController controller;


    @Test
    public void getLocalGovernment_should_return_a_local_goverment(){
        // given
        long localGovernmentId = 101L;

        // when
        Optional<LocalGovernment> localGovernment = controller.getLocalGovernment(localGovernmentId);

        // then
        assertThat(localGovernment.isPresent()).isTrue();
        assertThat(localGovernment.get().getName()).isEqualTo("Béchy");
        assertThat(localGovernment.get().getOverlappingLocalGovernment(LocalGovernmentType.FRANCE_INTERCOMMUNALITE).getId()).isEqualTo(201L);
        assertThat(localGovernment.get().getOverlappingLocalGovernment(LocalGovernmentType.FRANCE_INTERCOMMUNALITE).getName()).isEqualTo("CC Sud Messin");
    }

    @Test
    public void searchLocalGovernmentByName_should_return_a_list_of_local_governments(){
        // given
        String nameBeginning = "Bé";

        // when
        List<LocalGovernment> localGovernments = controller.searchLocalGovernmentByName(nameBeginning);

        // then
        assertThat(localGovernments).hasSize(2);
        assertThat(localGovernments).anyMatch(localGovernment -> localGovernment.getName().equals("Béchy"));
        assertThat(localGovernments).anyMatch(localGovernment -> localGovernment.getName().equals("Béthune"));
    }

    @Test
    public void getLocalGovernmentByWebSite_should_return_a_local_government(){
        // given
        String webSite = "www.bechy.fr";

        // when
        Optional<LocalGovernment> localGovernment = controller.getLocalGovernmentByWebSite(webSite);

        // then
        assertThat(localGovernment.isPresent()).isTrue();
        assertThat(localGovernment.get().getName()).isEqualTo("Béchy");
    }

    @Test
    public void getWebDocumentsByLocalGovernment_should_return_a_list_of_web_documents(){
        // given
        long localGovernmentId = 101L;

        // when
        List<WebDocument> webDocuments = controller.getWebDocumentsByLocalGovernment(localGovernmentId);

        // then
        assertThat(webDocuments).hasSize(2);
        assertThat(webDocuments).anyMatch(webDocument -> (webDocument.getId().equals("301") && webDocument.getUrl().equals("http://doc1.pdf")));
        assertThat(webDocuments).anyMatch(webDocument -> (webDocument.getId().equals("302") && webDocument.getUrl().equals("http://doc2.pdf")));
    }
}
