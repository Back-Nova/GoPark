import { Component } from '@angular/core';
import { Router } from '@angular/router'; // Importacion

@Component({
  selector: 'app-pagina-prin',
  imports: [],
  templateUrl: './pagina-prin.html',
  styleUrls: ['./pagina-prin.css']
})
export class PaginaPrin {

    constructor(private router: Router) {} // Se agrega el router

    Valogin() { // se agrega metodo
      this.router.navigate(['/login']);
    }
    Carrito(){
      this.router.navigate(['/carrito']);
    }
}