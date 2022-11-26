<template>
  <div id="app">
    RC Car Data
    <div class="content">
      <AccelChart msg="RC STATE"/>
      <SpeedChart />
    </div>
  </div>
</template>

<script>
import AccelChart from './components/AccelChart.vue'
import SpeedChart from './components/SpeedChart.vue'

export default {
  name: 'App',
  components: {
    AccelChart,
    SpeedChart
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  height:100vh;
  display: flex;
  flex-direction: column;
  margin-top:5%;
  font-size: 3rem;
  font-weight: bold;
}

.content{
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10%;
  font-size: 1rem;
}
</style>
