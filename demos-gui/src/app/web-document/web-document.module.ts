import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WebDocumentListComponent } from './components/web-document-list/web-document-list.component';

@NgModule({
  declarations: [
    WebDocumentListComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    WebDocumentListComponent
  ]
})
export class WebDocumentModule { }
