import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-local-government',
  templateUrl: './local-government.component.html',
  styleUrls: ['./local-government.component.css']
})
export class LocalGovernmentComponent implements OnInit {

  myControl = new FormControl();
  options: string[] = ['One', 'Two', 'Three'];
  constructor() { }

  ngOnInit(): void {
    console.log('LocalGovernmentComponent init');
  }

}
