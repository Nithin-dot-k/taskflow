import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  // This is our single point of truth for the backend URL
  private apiUrl = 'http://127.0.0.1:8000/auth'; 

  // We "inject" HttpClient here so we can use it to make requests
  constructor(private http: HttpClient) {}

  signup(userData: any): Observable<any> {
    // This sends the JSON data to our FastAPI /auth/signup endpoint
    return this.http.post(`${this.apiUrl}/signup`, userData);
  }
}