import { Component } from '@angular/core';
import { Router } from '@angular/router'; // Importacion

@Component({
  selector: 'app-carrito',
  imports: [],
  templateUrl: './carrito.html',
  styleUrl: './carrito.css'
})
export class Carrito {
  constructor(private router: Router) {} // Se agrega el router

  PaginaPrincipal() { // se agrega metodo
    this.router.navigate(['/']);
  }

}
