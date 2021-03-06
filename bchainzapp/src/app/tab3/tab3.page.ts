import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-tab3',
  templateUrl: 'tab3.page.html',
  styleUrls: ['tab3.page.scss']
})
export class Tab3Page {

  deposit: boolean = true;

  amount: number = 0;
  balance = 0;

  constructor(public http: HttpClient) {
  }

  ionViewWillEnter() {
    this.http.get<any>('http://3.120.6.183:5000/api/getBalanceUser').subscribe(r => {
      this.balance = r.Data;
    });

  }

  withdraw(){
    this.http.get<any>('http://3.120.6.183:5000/api/withdrawUser?amount='+String(this.amount)).subscribe(r1 => {
      if (r1.Response != '200') {
        console.log('Something happened, please try again later')
      }
    });
  }

}
