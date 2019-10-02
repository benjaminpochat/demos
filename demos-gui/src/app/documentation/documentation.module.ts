import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PresentationComponent } from './presentation/components/presentation.component';

@NgModule({
  declarations: [
    PresentationComponent
  ],
  imports: [
    CommonModule,
  ],
  exports: [
    PresentationComponent
  ]
})
export class DocumentationModule { }
