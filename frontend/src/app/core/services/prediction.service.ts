import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class PredictionService {
  private baseUrl = 'http://localhost:5000/api/predictions';

  constructor(private http: HttpClient) {}

  getPredictions(): Observable<any> {
    return this.http.get(`${this.baseUrl}`);
  }
}
