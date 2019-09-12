import { Component, OnInit, EventEmitter, Output } from '@angular/core';
import { FormControl } from '@angular/forms';
import { LocalGovernmentService } from '../../services/local-government.service';
import { startWith, debounceTime, distinctUntilChanged, filter } from 'rxjs/operators';
import { LocalGovernment } from '../../model/local-government.model';
import { MatOption } from '@angular/material/core';
import { WebDocument } from 'src/app/web-document/model/web-document.model';
import { Observable } from 'rxjs';
import { MatAutocomplete } from '@angular/material/autocomplete';

@Component({
  selector: 'app-local-government-selector',
  templateUrl: './local-government-selector.component.html',
  styleUrls: ['./local-government-selector.component.css']
})

export class LocalGovernmentSelectorComponent implements OnInit {

  constructor( private service: LocalGovernmentService) {
  }

  localGovernmentSelectorControl: FormControl = new FormControl('');
  displayedLocalGovernments: Array<LocalGovernment>;
  @Output() selected = new EventEmitter<Array<WebDocument>>();

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

  selectLocalGovernement(selectedOption: MatOption) {
    this.localGovernmentSelectorControl.setValue(selectedOption.getLabel());
    const selectedLocalGovernment = new LocalGovernment();
    selectedLocalGovernment.id = Number(selectedOption.value).valueOf();
    this.service.getWebDocuments(selectedLocalGovernment)
      .subscribe((webDocuments: Array<WebDocument>) => this.selected.emit(webDocuments));
  }
}
