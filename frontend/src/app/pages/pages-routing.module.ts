import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardsComponent } from './dashboards/dashboards.component';
import { MatchingComponent } from './matching/matching.component';
import { AlerteComponent } from './alerte/alerte.component';
import { RecommendationComponent } from './recommendation/recommendation.component';
import { PredictionComponent } from './prediction/prediction/prediction.component';
import { DashboardRhComponent } from './dashboard-rh/dashboard-rh.component';
import { ɵINTERNAL_BROWSER_DYNAMIC_PLATFORM_PROVIDERS } from '@angular/platform-browser-dynamic';



const routes: Routes = [
  {
    path: 'tables',
    loadChildren: () => import('./tables/tables.module').then(m => m.TablesModule)
  },
  { path: 'dashboard', component: DashboardsComponent },
  { path: 'matching', component: MatchingComponent },
  {path :'alerte', component:AlerteComponent},
  {path:'recommendation',component:RecommendationComponent},
  {path:'predict',component:PredictionComponent},
  {path:'rapport',component:DashboardRhComponent}

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PagesRoutingModule { }
