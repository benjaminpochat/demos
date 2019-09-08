package org.demos.core.domains.localgovernment;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ThreadLocalRandom;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

@RestController
public class LocalGovernmentController {

    @Autowired
    private LocalGovernmentRepository localGovernmentRepository;

    @GetMapping(path = "/localGovernments/forScraping")
    public List<LocalGovernment> getLocalGovernmentForScraping(@RequestParam(value = "size") int size){
        long nbLocalGovernments = localGovernmentRepository.countLocalGovernmentsWithWebSite();
        Iterator<LocalGovernment> allLocalGovernmentsIterator = localGovernmentRepository.findByWebSiteIsNotNull().iterator();
        List<Long> randomLocalGovernmentIndices = IntStream.range(0, size).mapToObj(b -> ThreadLocalRandom.current().nextLong(1, nbLocalGovernments)).sorted().collect(Collectors.toList());
        return selectSomeLocalGovernment(allLocalGovernmentsIterator, randomLocalGovernmentIndices);
    }

    @GetMapping(path = "/localGovernments/{id}")
    public Optional<LocalGovernment> getLocalGovernment(@PathVariable Long id){
        return localGovernmentRepository.findById(id);
    }

    @GetMapping(path = "/localGovernments/searchByName/{name}")
    public List<LocalGovernment> searchLocalGovernmentByName(@PathVariable String name){
        return localGovernmentRepository.findFirst20ByNameStartingWithIgnoreCase(name, Sort.by("name"));
    }

    @GetMapping(path= "/localGovernments")
    public Optional<LocalGovernment> getLocalGovernmentByWebSite(@RequestParam(value = "webSite") String webSite){
        return localGovernmentRepository.findByWebSite(webSite);
    }

    List<LocalGovernment> selectSomeLocalGovernment(Iterator<LocalGovernment> allGovernmentsIterator, List<Long> selectedLocalGovernmentsIndices) {
        List<LocalGovernment> selectedGovernments = new ArrayList<>();
        long allGovernmentsIteratorCursor = 1;
        int selectedGovernementsIndicesCursor = 0;
        while(allGovernmentsIterator.hasNext() && selectedGovernementsIndicesCursor < selectedLocalGovernmentsIndices.size()){
            LocalGovernment localGovernment = allGovernmentsIterator.next();
            if(allGovernmentsIteratorCursor == selectedLocalGovernmentsIndices.get(selectedGovernementsIndicesCursor)){
                selectedGovernments.add(localGovernment);
                selectedGovernementsIndicesCursor++;
            }
            allGovernmentsIteratorCursor++;
        }
        return selectedGovernments;
    }
}
