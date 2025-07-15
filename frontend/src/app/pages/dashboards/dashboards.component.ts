import { Component, OnInit, OnDestroy } from '@angular/core';
import { DashboardService } from 'src/app/core/services/dashboard';
import * as am5 from '@amcharts/amcharts5';
import * as am5map from '@amcharts/amcharts5/map';
import am5geodata_franceLow from '@amcharts/amcharts5-geodata/franceLow';
import am5themes_Animated from '@amcharts/amcharts5/themes/Animated';



@Component({
  selector: 'app-dashboards',
  templateUrl: './dashboards.component.html',
})
export class DashboardsComponent implements OnInit, OnDestroy {
  dashboardData: any;
  startDate: string = '';
  endDate: string = '';
  consultantChartData: any;
  topJobs: any;
  topSkills: any;
  topSectors: any;
  topEntreprisesChart: any;
  experienceChart: any;
  contratsChart: any;
  evolutionChart: any;
  offreCount: number = 0;
  successRate: number = 0;
  totalConsultants: number = 0;
  private root: am5.Root | null = null;

  cityCoordinates: { [key: string]: { lat: number; lon: number } } = {
  "ile-de-france": { lat: 48.8499, lon: 2.6370 },
  "auvergne-rhone-alpes": { lat: 45.7640, lon: 4.8357 },
  "provence-alpes-cote d'azur": { lat: 43.9352, lon: 6.0679 },
  "paris": { lat: 48.8566, lon: 2.3522 },
  "lyon": { lat: 45.7640, lon: 4.8357 },
  "marseille": { lat: 43.2965, lon: 5.3698 },
  "toulouse": { lat: 43.6047, lon: 1.4442 },
  "nice": { lat: 43.7102, lon: 7.2620 },
  "nantes": { lat: 47.2184, lon: -1.5536 },
  "strasbourg": { lat: 48.5734, lon: 7.7521 },
  "montpellier": { lat: 43.6117, lon: 3.8777 },
  "bordeaux": { lat: 44.8378, lon: -0.5792 },
  "lille": { lat: 50.6292, lon: 3.0573 },
  "france": { lat: 46.603354, lon: 1.888334 }, // Central point
  "île-de-france": { lat: 48.8499, lon: 2.6370 },
  "azle-de-france": { lat: 48.8499, lon: 2.6370 }, // Corrected typo variant
  "auvergne-rhône-alpes": { lat: 45.7640, lon: 4.8357 }, // Lyon is capital
  "occitanie": { lat: 43.6047, lon: 1.4442 }, // Toulouse is capital
  "nouvelle-aquitaine": { lat: 44.8378, lon: -0.5792 }, // Bordeaux is capital
  "hauts-de-france": { lat: 50.6292, lon: 3.0573 }, // Lille
  "provence-alpes-côte d'azur": { lat: 43.2965, lon: 5.3698 }, // Marseille
};


  constructor(private dashboardService: DashboardService) {}

  ngOnInit(): void {
    this.loadDashboardData();
    
  }
  loadDashboardData(): void {
    this.dashboardService.getDashboardData(this.startDate, this.endDate).subscribe((data) => {
      this.dashboardData = data;
      console.log(this.dashboardData)
      this.offreCount = data.offre_count;
      this.successRate = data.success_rate;
      this.totalConsultants = Number(data.consultant_status.disponible) + Number(data.consultant_status.en_mission)+Number(data.consultant_status.inactif);

      this.consultantChartData = {
        series: [
          Number(data.consultant_status.disponible),
          Number(data.consultant_status.en_mission),
          Number(data.consultant_status.inactif),
        ],
        chart: {
          type: "pie",
          height: 300
        },
        labels: ["Disponible", "En mission", "Inactif"],
        colors: ["#28a745", "#007bff", "#dc3545"],
        legend: {
          position: "bottom",
        },
      };

      this.topJobs = {
        title: "Top Jobs",
        categories: data.top_jobs.map((x: any) => x.nom),
        data: data.top_jobs.map((x: any) => x.total_occurences),
        chartType: 'donut'
      };

      this.topSkills = {
        title: "Top Compétences",
        categories: data.top_skills.map((x: any) => x.top_skills),
        data: data.top_skills.map((x: any) => x.total_occurences),
        chartType: 'bar'
      };

      this.topSectors = {
        title: "Top Secteurs",
        categories: data.top_secteurs.map((x: any) => x.nom),
        data: data.top_secteurs.map((x: any) => Number(x.total_occurences)),
        chartType: 'donut'
      };

      this.topEntreprisesChart = this.getDonutChartOptions((data.top_entreprises));
      
    

     
     
      this.renderMap(data.offres_par_localisation);
    });
  }
  

  renderMap(locations: any[]): void {
  if (this.root) this.root.dispose();
  this.root = am5.Root.new("chartdiv");
  this.root.setThemes([am5themes_Animated.new(this.root)]);

  const chart = this.root.container.children.push(
    am5map.MapChart.new(this.root, {
      panX: "none",
      panY: "none",
      projection: am5map.geoMercator(),
    })
  );

  // Removed auto zoom and center calls here

  chart.series.push(
    am5map.MapPolygonSeries.new(this.root, {
      geoJSON: am5geodata_franceLow,
      exclude: ["AQ"],
    })
  );

  const pointSeries = chart.series.push(
    am5map.MapPointSeries.new(this.root, {
      valueField: "value",
      calculateAggregates: true,
    })
  );

  pointSeries.bullets.push((root, series, dataItem) => {
    const radius = 6 + (dataItem.get("value") || 0);
    const circle = am5.Circle.new(root, {
      radius: radius,
      fill: am5.color(0xff6b00),
      tooltipText: "{city}: {value} offres",
    });

    return am5.Bullet.new(root, {
      sprite: circle,
    });
  });

  const data = [];

  locations.forEach((loc) => {
    const cityKey = this.normalize(loc.location.trim());
    const coords = this.cityCoordinates[cityKey];
    console.log(`Adding point for ${loc.location}: value = ${loc.total}`, coords);
    if (coords) {
      data.push({
        longitude: coords.lon,
        latitude: coords.lat,
        value: loc.total,
        city: loc.location,
      });
    } else {
      console.warn("No coordinates for:", loc.location);
    }
  });

  pointSeries.data.setAll(data);
}

  normalize(str: string): string {
  return str.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

  getDonutChartOptions(data: any[]): any {
      return {
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'horizontal',
          top: 5,
          formatter: '{name}',
        },
        series: [
          {
            name: 'Entreprises',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
              show: true,
              position: 'inside',
              formatter: '{c}', // Affiche la valeur au centre
              fontWeight: 'bold',
              fontSize: 14,
              color: '#fff'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 18,
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: data.map((item, index) => ({
              name: item.company_name,
              value: item.total
            }))
          }
        ]
      };
    }


  ngOnDestroy(): void {
    if (this.root) {
      this.root.dispose();
    }
  }

  applyDateFilter() {
    this.loadDashboardData();
  }
}