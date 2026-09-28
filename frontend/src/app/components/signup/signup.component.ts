import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
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
  constructor(private authService: AuthService) {}

  onSignup() {
    const userData = { email: this.email, password: this.password };

    // Here we use the service!
    this.authService.signup(userData).subscribe({
      next: (response) => console.log('Signup successful!', response),
      error: (err) => console.error('Signup failed', err),
    });
  }
}
