import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css'],
})
export class SignupComponent {
  email = '';
  password = '';

  // Injection happens here!
  constructor(private authService: AuthService, private router: Router) {}

  onSignup() {
    const userData = { email: this.email, password: this.password };

  // 1. Create the account in PostgreSQL
  this.authService.signup(userData).subscribe({
    next: () => {
      // 2. Immediately log in in the background!
      this.authService.login(this.email, this.password).subscribe({
        next: (loginResponse) => {
          localStorage.setItem('token', loginResponse.access_token);
          // 3. Take them directly to the app!
          this.router.navigate(['/projects']);
        },
        error: () => this.router.navigate(['/login'])
      });
    },
    error: (err) => alert("Signup failed. That email might already be taken.")
  });
  }
}
