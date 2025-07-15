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
export class DashboardsComponent implements OnInit, OnDestroy  {
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
  "paysdelaloire": { lat: 47.7633, lon: -0.3286 }, 
  "nanterre": { lat: 48.8924, lon: 2.2060 },
  "grandest": { lat: 48.6997, lon: 6.1876 },
  "saintmarcel": { lat: 49.1021, lon: 1.4882 }, 
  "bretagne": { lat: 48.2020, lon: -2.9326 },
  "courbevoie": { lat: 48.8967, lon: 2.2573 },
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
  "france": { lat: 46.603354, lon: 1.888334 }, 
  "île-de-france": { lat: 48.8499, lon: 2.6370 },
  "azle-de-france": { lat: 48.8499, lon: 2.6370 }, 
  "auvergne-rhône-alpes": { lat: 45.7640, lon: 4.8357 }, 
  "occitanie": { lat: 43.6047, lon: 1.4442 }, 
  "nouvelle-aquitaine": { lat: 44.8378, lon: -0.5792 }, 
  "hauts-de-france": { lat: 50.6292, lon: 3.0573 }, 
  "provence-alpes-côte d'azur": { lat: 43.2965, lon: 5.3698 },
};
  data: { city: string; latitude: number; longitude: number; value: number; }[];


  constructor(private dashboardService: DashboardService) {}
  ngAfterViewInit(): void {
    throw new Error('Method not implemented.');
  }

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
  if (this.root) this.root.dispose();
  this.root = am5.Root.new("chartdiv");
  this.root.setThemes([am5themes_Animated.new(this.root)]);

  const chart = this.root.container.children.push(
    am5map.MapChart.new(this.root, {
      panX: "none",
      panY: "none",
      wheelY: 'zoom',
      projection: am5map.geoMercator(),
    })
  );

  let polygonSeries = chart.series.push(
      am5map.MapPolygonSeries.new(this.root, {
        geoJSON: am5geodata_franceLow,
        exclude: ['AQ'],
      })
    );

    let pointSeries = chart.series.push(
  am5map.MapPointSeries.new(this.root, {
    valueField: "value",
    latitudeField: "latitude",
    longitudeField: "longitude"
  })
);

pointSeries.bullets.push((root, series, dataItem) => {
  return am5.Bullet.new(root, {
    sprite: am5.Circle.new(root, {
      radius: 6,
      fill: am5.color(0xff0000),
      tooltipText: "{city}: {value}"
    })
  });
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