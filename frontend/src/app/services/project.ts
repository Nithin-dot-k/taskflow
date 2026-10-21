import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ProjectService {
  private apiUrl = 'http://127.0.0.1:8000/projects';

  constructor(private http: HttpClient) {}

  getProjects(): Observable<any> {
    // 1. Retrieve the token we saved during login
    const token = localStorage.getItem('token');

    // 2. Create headers
    // If there is no token, this will be empty, which is fine
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });

    // 3. Send headers along with the GET request
    return this.http.get(`${this.apiUrl}/`, { headers });
  }
}
