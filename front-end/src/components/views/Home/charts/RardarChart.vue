<template>
  <radar-chart
    :options="chartOptions"
    :data="chartData"
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :plugins="plugins"
    :css-classes="cssClasses"
    :styles="styles"
    :width="width"
    :height="height"
  />
</template>
  
<script>
import { Radar as RadarChart } from "vue-chartjs";

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
  RadialLinearScale,
  Filler,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  PointElement,
  RadialLinearScale,
  LineElement,
  Filler
);

export default {
  name: "RadarChart",
  components: {
    "radar-chart": RadarChart,
  },
  props: {
    chartId: {
      type: String,
      default: "radar-chart",
    },
    datasetIdKey: {
      type: String,
      default: "label",
    },
    width: {
      type: Number,
      default: 300,
    },
    height: {
      type: Number,
      default: 300,
    },
    cssClasses: {
      default: "",
      type: String,
    },
    styles: {
      type: Object,
      default: () => {},
    },
    plugins: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    chartData() {
      return {
        labels: [
          "Angle_id: 1",
          "Angle_id: 2",
          "Angle_id: 3",
          "Angle_id: 4",
          "Angle_id: 5",
          "Angle_id: 6",
          "Angle_id: 7",
        ],
        datasets: [
          {
            label: "Total number of routers with 'fail' status",
            data: this.$store.state.chartDashboard.stateFail,
            backgroundColor: "rgba(190, 52, 85, 0.3)",
            borderColor: "#BE3455",
            borderWidth: 1,
            pointBackgroundColor: "#BE3455",
            pointBorderColor: "white",
            pointBorderWidth: 0,
            pointRadius: 3,
            fill: {
              target: "origin",
              above: "rgba(190, 52, 85, 0.3)", // Area will be red above the origin
              below: "rgba(190, 52, 85, 0.3)", // And blue below the origin
            },
          },
          {
            label: "Total number of routers with 'ok' status",
            data: this.$store.state.chartDashboard.stateOk,
            backgroundColor: "rgba(26, 178, 167, 0.5)",
            borderColor: "#1AB2A7",
            borderWidth: 1,
            pointBackgroundColor: "#1AB2A7",
            pointBorderColor: "white",
            pointBorderWidth: 0,
            pointRadius: 3,
            fill: {
              target: "origin",
              above: "rgba(26, 178, 167, 0.5)", // Area will be red above the origin
              below: "rgba(26, 178, 167, 0.5)", // And blue below the origin
            },
          },
        ],
      };
    },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: {
              // This more specific font property overrides the global property
              font: {
                size: 14,
              },
            },
          },
        },
      };
    },
  },
};
</script>
  