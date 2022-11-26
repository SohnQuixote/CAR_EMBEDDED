<template>
  <div class="line">
    Temperature / Humidity
    <apexchart width="700" type="line" :options="options" :series="series" />
  </div>
</template>

<script>
import io from 'socket.io-client'
import VueApexCahrts from 'vue-apexcharts'
import moment from 'moment'

export default {
  name: 'AccelChart',
  props: {
    msg: String,
  },
  components:{
    apexchart: VueApexCahrts,
  },
  data(){
    return {
      socket: '',
      time: [],
      temperatures: [],
      humidities: [],
      options: {},
      series: [],
    }
  },
   created(){
    this.socket = io("http://localhost:3000")
    this.socket.on("result", (arg)=>{
      console.log(arg);
      this.times = arg.slice(0).reverse().map((x) => moment(x.time).format("mm:ss"));
      this.temperatures = arg.slice(0).reverse().map((x) => Math.round(x.temperature * 10) / 10);
      this.humidities = arg.slice(0).reverse().map((x) => Math.round(x.humidity * 10) / 10);
      this.options = {
        chart: {
          height: 350,
          type: 'line',
          // stacked: false,
        },
        stroke: {
          width: [0, 2, 5],
          curve: 'smooth'
        }, 
        fill: {
          type: "solid",
          opacity: [0.35, 1]
        },
        labels: this.times,
        markers: {
          size: 0
        },
        xaxis: {
          type: 'Time'
        },
        yaxis: [
        {
          title: {
            text: "Temperature (degree)",
          },
          max: 40,
          min: 25
        },
        {
          opposite: true,
          title: {
            text: "Humidity (%)",
          },
          max: 40,
          min: 25
        }
      ],
        tooltip: {
          shared: true,
          intersect: false,
          y: {
            formatter: function (y) {
              if (typeof y !== "undefined") {
                return y.toFixed(0) + " points";
              }
              return y;
        
            }
          }
        },
      };
      this.series = [
       
        {
          name: "습도",
          type: 'area',
          data: this.humidities,
        },
        {
          name: "온도",
          type: 'line',
          data: this.temperatures,
        },
      ]
     })

    this.socket.emit("connection", "success");
  }
}
</script>

<style scoped>
</style>