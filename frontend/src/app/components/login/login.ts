import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  email = '';
  password = '';

  constructor(private authService: AuthService) {}

  onLogin() {
    // 1. Call the service
    this.authService.login(this.email, this.password).subscribe({
      next: (response) => {
        // 2. Save the token in the browser's persistent storage
        localStorage.setItem('token', response.access_token);
        alert('Login successful!');
      },
      error: (err) => alert('Login failed. Check your credentials.'),
    });
  }
}
