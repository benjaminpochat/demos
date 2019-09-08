import { Component, OnInit } from '@angular/core';
import { GlobalStatistics } from '../model/global-statistics.model';
import { GlobalStatisticsService } from '../services/global-statistics.service';

@Component({
  selector: 'app-global-statistics',
  templateUrl: './global-statistics.component.html',
  styleUrls: ['./global-statistics.component.css']
})
export class GlobalStatisticsComponent implements OnInit {

  globalStatistics: GlobalStatistics = new GlobalStatistics();

  constructor( private service: GlobalStatisticsService) {
    console.log('GlobalStatisticsComponent#constructor');
  }

  ngOnInit() {
    this.service.getGlobalStatistics<any>().subscribe(
      (data: any) => this.globalStatistics = data,
      error => () => {
        console.log('Error at GlobalStatisticsComponent#ngOnInit');
      }
    );
  }

}
