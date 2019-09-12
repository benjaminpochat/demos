import { Component, OnInit, Input } from '@angular/core';
import { WebDocument } from '../../model/web-document.model';

@Component({
  selector: 'app-web-document-list',
  templateUrl: './web-document-list.component.html',
  styleUrls: ['./web-document-list.component.css']
})
export class WebDocumentListComponent {

  constructor() { }

  @Input() webDocuments = new Array<WebDocument>();
  @Input() localGovernmentSelected = false;

}
