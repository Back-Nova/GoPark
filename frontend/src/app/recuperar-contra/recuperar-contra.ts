import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-recuperar-contra',
  imports: [],
  templateUrl: './recuperar-contra.html',
  styleUrl: './recuperar-contra.css'
})
export class RecuperarContra {
  constructor(private router: Router) {} // Se agrega el router
    Login() { // se agrega metodo
      this.router.navigate(['/login']);
    }

}
