import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DashboardRHService {

  private baseUrl = 'http://localhost:5000/api/dashboard_rh/relations';

  constructor(private http: HttpClient) {}

  getRelations(startDate?: string, endDate?: string) {
    let params = new HttpParams();
    if (startDate) {
      params = params.set('start_date', startDate);
    }
    if (endDate) {
      params = params.set('end_date', endDate);
    }

    return this.http.get<any>(`${this.baseUrl}`, { params });
  }
}

