import { Component } from '@angular/core';
import { WebDocument } from './web-document/model/web-document.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'Demos';
  webDocuments = new Array<WebDocument>();
  localGovernmentSelected = false;

  onLocalGovernmentSelected(webDocuments: Array<WebDocument>) {
    console.log('AppComponent#onLocalGovernmentSelected');
    console.log(webDocuments);
    this.webDocuments = webDocuments;
    this.localGovernmentSelected = true;

  }
}
