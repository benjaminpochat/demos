package org.demos.core.domains.localgovernment;

import org.junit.Test;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static org.assertj.core.api.Assertions.assertThat;

public class TestLocalGovernmentController {

/*    @Test
    public void selectSomeLocalGovernment_should_return_a_list_of_local_governments(){
        // given
        LocalGovernmentController controller = new LocalGovernmentController();
        List<LocalGovernment> localGovernments = IntStream.range(1, 10).mapToObj(i -> new LocalGovernment()).collect(Collectors.toList());
        List<Long> selectedLocalGovernmentsIndices = Arrays.asList(3L, 4L, 8L);

        // when
        List<LocalGovernment> selectedLocalGovernments = controller.selectSomeLocalGovernment(localGovernments.iterator(), selectedLocalGovernmentsIndices);

        // then
        assertThat(selectedLocalGovernments).containsExactlyInAnyOrder(localGovernments.get(2), localGovernments.get(3), localGovernments.get(7));
    }

    @Test
    public void selectSomeLocalGovernment_should_return_a_list_of_local_governments_if_the_same_index_given_twice(){
        // given
        LocalGovernmentController controller = new LocalGovernmentController();
        List<LocalGovernment> localGovernments = IntStream.range(1, 10).mapToObj(i -> new LocalGovernment()).collect(Collectors.toList());
        List<Long> selectedLocalGovernmentsIndices = Arrays.asList(3L, 4L, 3L);

        // when
        List<LocalGovernment> selectedLocalGovernments = controller.selectSomeLocalGovernment(localGovernments.iterator(), selectedLocalGovernmentsIndices);

        // then
        assertThat(selectedLocalGovernments).containsExactlyInAnyOrder(localGovernments.get(2), localGovernments.get(3));
    }*/

}
