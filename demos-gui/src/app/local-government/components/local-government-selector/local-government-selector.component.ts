import { Component, OnChanges, SimpleChanges, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { LocalGovernmentService } from '../../services/local-government.service';
import { startWith, debounceTime, distinctUntilChanged, filter } from 'rxjs/operators';
import { LocalGovernment } from '../../model/local-government.model';
import { MatOption } from '@angular/material/core';

@Component({
  selector: 'app-local-government-selector',
  templateUrl: './local-government-selector.component.html',
  styleUrls: ['./local-government-selector.component.css']
})

export class LocalGovernmentSelectorComponent implements OnInit {

  constructor( private service: LocalGovernmentService) {
  }

  localGovernmentSelectorControl: FormControl = new FormControl('');
  selectedLocalGovernment: LocalGovernment;
  displayedLocalGovernments: Array<LocalGovernment>;

  ngOnInit(): void {
    this.localGovernmentSelectorControl.valueChanges
      .pipe(
        startWith(''),
        debounceTime(400),
        distinctUntilChanged(),
        filter((searchedName: string) => searchedName.length > 0)
    ).subscribe((searchedName: string) => this.searchLocalGovernments(searchedName));
  }

  private searchLocalGovernments(searchedName: string) {
    this.service.searchLocalGovernments(searchedName)
      .subscribe(
        (localGovernments: Array<LocalGovernment>) => this.displayedLocalGovernments = localGovernments);
  }

  updateSearchedName(selectedOption: MatOption) {
    this.localGovernmentSelectorControl.setValue(selectedOption.getLabel());
  }
}
