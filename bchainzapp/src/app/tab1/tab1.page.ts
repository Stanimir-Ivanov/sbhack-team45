import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page {

  balance = 0;

  constructor(public http: HttpClient) {
    http.get<any>('http://3.120.6.183:5000/api/getBalanceUser').subscribe(r => {
      this.balance = r.Data;
    });
  }

}
