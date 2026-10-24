import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TaskService {
  private apiUrl = 'http://127.0.0.1:8000/tasks';

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  // Fetch tasks belonging to a specific project
  getTasks(projectId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/?project_id=${projectId}`, {
      headers: this.getHeaders()
    });
  }

  // Create a new task attached to a project
  createTask(taskData: { title: string; description?: string; project_id: number }): Observable<any> {
    return this.http.post(`${this.apiUrl}/`, taskData, {
      headers: this.getHeaders()
    });
  }
}
