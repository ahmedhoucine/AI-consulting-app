import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FeedbackService {
  private apiUrl = 'http://localhost:5000/feedbacks';  

  constructor(private http: HttpClient) {}

  getFeedbacks(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }
}
