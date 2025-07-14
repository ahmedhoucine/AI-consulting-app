import { Component, OnInit } from '@angular/core';
import {
  ApexAxisChartSeries,
  ApexChart,
  ApexXAxis,
  ApexTitleSubtitle,
  ApexDataLabels,
  ApexStroke,
  ApexTooltip,
  ApexLegend,
  ApexMarkers,
  ApexNonAxisChartSeries,
  ApexPlotOptions
} from "ng-apexcharts";
import { DashboardRHService } from 'src/app/core/services/dashboard_rh';

export type ChartOptions = {
  series: ApexAxisChartSeries | ApexNonAxisChartSeries;
  chart: ApexChart;
  xaxis?: ApexXAxis;
  title?: ApexTitleSubtitle;
  dataLabels?: ApexDataLabels;
  stroke?: ApexStroke;
  tooltip?: ApexTooltip;
  legend?: ApexLegend;
  markers?: ApexMarkers;
  labels?: string[];
  plotOptions?: ApexPlotOptions;
};

@Component({
  selector: 'app-dashboard-rh',
  templateUrl: './dashboard-rh.component.html',
  styleUrls: ['./dashboard-rh.component.scss']
})
export class DashboardRhComponent implements OnInit {
  startDate?: string;
  endDate?: string;
  selectedLocalisation?: string;
  localisations: string[] = [];

  chartSalaireCourbes?: ChartOptions;
  chartContrats?: ChartOptions;
  chartCandidats?: ChartOptions;

  chartEvolutionPublication?: ChartOptions;

  constructor(private dashboardService: DashboardRHService) {}

  ngOnInit(): void {
    this.loadData();
  }

  applyDateFilter(): void {
    this.loadData();
  }

  onLocalisationChange(): void {
    this.loadSalaireCurves();
  }

  loadData(): void {
    this.dashboardService.getRelations(this.startDate, this.endDate).subscribe({
      next: (response) => {
        const data = response.data || {};

        const salaires = data.salaires_par_localisation_et_secteur || [];
        this.localisations = salaires.map((loc: any) => loc.localisation);
        if (!this.selectedLocalisation && this.localisations.length > 0) {
          this.selectedLocalisation = this.localisations[0];
        }

        this.buildSalaireCourbes(salaires);
        this.buildContratsChart(data.types_contrat_par_secteur || []);
        this.buildCandidatsChart(data.candidats_par_secteur || []);
        this.buildEvolutionChart(data.evolution_publication_par_secteur || []);
      },
      error: (err) => {
        console.error('Erreur chargement dashboard RH :', err);
      }
    });
  }

  buildSalaireCourbes(salairesData: any[]): void {
    const locData = salairesData.find((l: any) => l.localisation === this.selectedLocalisation);
    if (!locData) return;

    const secteurs = locData.secteurs.map((s: any) => s.secteur);
    const minSalaire = locData.secteurs.map((s: any) => s.min_salaire);
    const maxSalaire = locData.secteurs.map((s: any) => s.max_salaire);

    this.chartSalaireCourbes = {
      series: [
        { name: "Salaire Min", data: minSalaire },
        { name: "Salaire Max", data: maxSalaire }
      ],
      chart: { height: 350, type: "line", zoom: { enabled: false } },
      dataLabels: { enabled: true },
      stroke: { curve: "smooth" },
      title: { text: `Salaires par secteur - ${this.selectedLocalisation}` },
      xaxis: { categories: secteurs },
      tooltip: { shared: true, intersect: false },
      legend: { position: "top" },
      markers: { size: 4 }
    };
  }

  buildContratsChart(data: any[]): void {
    const secteurs = Array.from(new Set(data.map(d => d.secteur)));
    const types = Array.from(new Set(data.map(d => d.type_contrat)));

    const series = secteurs.map(secteur => {
      return {
        name: secteur,
        data: types.map(type => {
          const match = data.find(d => d.secteur === secteur && d.type_contrat === type);
          return match ? match.count : 0;
        })
      };
    });

    this.chartContrats = {
      series,
      chart: { type: 'bar', height: 450, stacked: true, toolbar: { show: true } },
      title: { text: 'Types de contrat par secteur' },
      xaxis: {
        categories: types,
        labels: { rotate: -45, style: { fontSize: '12px' } }
      },
      legend: { position: 'top', horizontalAlign: 'left' },
      tooltip: { shared: true, intersect: false }
    };
  }

  

 

  buildEvolutionChart(data: any[]): void {
    const secteurs = Array.from(new Set(data.map(d => d.secteur)));
    const dates = Array.from(new Set(data.map(d => d.date))).sort();

    const series = secteurs.map(secteur => {
      return {
        name: secteur,
        data: dates.map(date => {
          const match = data.find(d => d.date === date && d.secteur === secteur);
          return match ? match.count : 0;
        })
      };
    });

    this.chartEvolutionPublication = {
      series,
      chart: { type: 'line', height: 450, toolbar: { show: true }, zoom: { enabled: true } },
      xaxis: { categories: dates },
      title: { text: 'Évolution des publications par secteur' },
      stroke: { curve: 'smooth', width: 2 },
      legend: { position: 'top' },
      markers: { size: 3 },
      tooltip: { shared: true, intersect: false }
    };
  }

  buildCandidatsChart(data: any[]): void {
    const total = data.reduce((sum, d) => sum + d.nombre_candidats, 0);
    const filtered = data.filter(d => d.nombre_candidats > total * 0.01);
    this.chartCandidats = {
      series: filtered.map(d => d.nombre_candidats),
      chart: { type: 'donut', height: 400 },
      labels: filtered.map(d => d.secteur),
      title: { text: 'Candidats par secteur' },
      legend: { position: 'bottom' }
    };
  }

  loadSalaireCurves(): void {
    this.dashboardService.getRelations(this.startDate, this.endDate).subscribe({
      next: (response) => {
        const salaires = response.data?.salaires_par_localisation_et_secteur || [];
        this.buildSalaireCourbes(salaires);
      },
      error: (err) => {
        console.error('Erreur rafraîchissement salaires :', err);
      }
    });
  }
}
