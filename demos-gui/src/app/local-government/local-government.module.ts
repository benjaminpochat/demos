import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { LocalGovernmentSelectorComponent } from './components/local-government-selector/local-government-selector.component';

import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatAutocompleteModule} from '@angular/material/autocomplete';
import { LocalGovernmentService } from './services/local-government.service';

@NgModule({
  declarations: [
    LocalGovernmentSelectorComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    MatInputModule,
    MatAutocompleteModule,
    MatFormFieldModule
  ],
  exports: [
    LocalGovernmentSelectorComponent
  ],
  providers: [
    LocalGovernmentService
  ]
})
export class LocalGovernmentModule { }
