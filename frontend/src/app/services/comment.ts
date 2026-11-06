import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CommentService {
  private apiUrl = 'http://127.0.0.1:8000/tasks';

  constructor(private http: HttpClient) {}

  // 1. GET /tasks/{task_id}/comments/
  getComments(taskId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/${taskId}/comments/`);
  }

  // 2. POST /tasks/{task_id}/comments/
  addComment(taskId: number, text: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${taskId}/comments/`, { text });
  }
}