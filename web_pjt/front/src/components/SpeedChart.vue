<template>
  <div>
    Accelerometer
    <div class="speed">
      <VueSvgGauge class="pan"
        :start-angle="-140"
        :end-angle="140"
        :value="acc_roll"
        :separator-step="1"
        :min="0"
        :max="400"
        :gauge-color="[{ offset: 0, color: '#347AB0'}, { offset: 100, color: '#8CDFAD'}]"
        :scale-interval="10"
        :separatorThickness="0"
      >
        <div class="inner-text">
          <p>{{acc_roll}} m/s2</p>
        </div>
      </VueSvgGauge>
      <VueSvgGauge class="pan"
        :start-angle="-140"
        :end-angle="140"
        :value="acc_yaw"
        :separator-step="1"
        :min="0"
        :max="400"
        :gauge-color="[{ offset: 0, color: '#347AB0'}, { offset: 100, color: '#8CDFAD'}]"
        :scale-interval="10"
        :separatorThickness="0"
      >
        <div class="inner-text">
          <p>{{acc_yaw}} m/s2</p>
        </div>
      </VueSvgGauge>
    </div>
  </div>
</template>

<script>
import io from 'socket.io-client'
import { VueSvgGauge } from 'vue-svg-gauge'

export default {
  name: 'SpeedChart',
  props: {
    msg: String,
  },
  components: {
    VueSvgGauge 
  },
  data(){
    return {
      socket: '',
      acc_roll: [],
      acc_yaw: [],
    }
  },
   created(){
    this.socket = io("http://localhost:3000")
    this.socket.on("result", (arg)=>{
      console.log(arg);
      this.acc_roll = Math.round(arg[0].acc_roll);
      this.acc_yaw = Math.round(arg[0].acc_yaw);
     })

    this.socket.emit("connection", "success");
  }
}
</script>

<style scoped>
  .speed{
    width:1000px;
    display: flex;
    justify-content: space-around;
    margin-top:50px;
  }

  .pan{
    width:400px;
  }

  .inner-text {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    height: 70%;
    width: 100%;
  }
</style>