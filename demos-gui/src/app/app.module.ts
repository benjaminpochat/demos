import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { MatInput } from '@angular/material/input';
import { MatFormField } from '@angular/material/form-field';
import { MatAutocomplete } from '@angular/material/autocomplete';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material';
import { MatSelect } from '@angular/material';

import { AppComponent } from './app.component';
import { LocalGovernmentComponent } from './local-government/local-government.component';

@NgModule({
  declarations: [
    AppComponent,
    LocalGovernmentComponent,
    MatInput,
    MatFormField,
    MatAutocomplete,
    MatSelect
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    MatSelectModule
  ],

  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
