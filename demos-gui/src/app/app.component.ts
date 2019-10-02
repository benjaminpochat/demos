import { Component } from '@angular/core';
import { WebDocument } from './web-document/model/web-document.model';
import { LocalGovernment } from './local-government/model/local-government.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'Demos';
  webDocuments = new Array<WebDocument>();
  localGovernmentSelected = false;
  localGovernment: LocalGovernment;

  onLocalGovernmentSelected(localGovernmentAndWebDocuments: [LocalGovernment, Array<WebDocument>]) {
    console.log('AppComponent#onLocalGovernmentSelected');
    if (localGovernmentAndWebDocuments) {
      console.log(localGovernmentAndWebDocuments[1]);
      this.localGovernment = localGovernmentAndWebDocuments[0];
      this.webDocuments = localGovernmentAndWebDocuments[1];
      this.localGovernmentSelected = true;
    }
  }
}
