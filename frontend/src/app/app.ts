import { Component, signal } from '@angular/core';
import { RouterOutlet, Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {

  constructor(private router: Router) {}

  // Check if a user currently has a token saved
  isLoggedIn(): boolean {
    return !!localStorage.getItem('token');
  }

  // Clear token and kick user back to login!
  logout() {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }
}
