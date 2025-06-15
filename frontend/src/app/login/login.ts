import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {
  constructor(private router: Router) {} // Se agrega el router

    Vaprin() { // se agrega metodo
      this.router.navigate(['/']);
    }
    
    Recuperar() { // se agrega metodo
      this.router.navigate(['/recuperar-contra']);
    }

  Registrar() {
    this.router.navigate(['/register']);
  }
}
