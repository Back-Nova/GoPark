import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-apartado-prin',
  imports: [],
  templateUrl: './apartado-prin.html',
  styleUrls: ['./apartado-prin.css']
})
export class ApartadoPrin {
  constructor(private router: Router) {} // Se agrega el router
  ApartadoPrin() { // se agrega metodo
    this.router.navigate(['/']);
  }

}
