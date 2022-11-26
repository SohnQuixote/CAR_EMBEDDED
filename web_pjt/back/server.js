
const express = require('express')
const app = express()
const cors = require("cors")
const port = 3000
const pool = require("./db")

const http = require('http')
const server = http.createServer(app)
const {Server} = require('socket.io')
const { json } = require('express')
const io = new Server(server, {
    cors:{
        origin: true
    },
    pingInterval: 100, 
    pingTimeout: 1
})

app.use(
    cors({
        origin:true,
    })
)

app.get('/', async (req, res)=>{

})

io.on("connection", async (socket)=>{
    const ret = await pool.query("select * from sensing order by time desc limit 15")
    socket.emit("result", ret[0])

    socket.on("connection", (arg)=>{
        console.log(arg);
    })
})

server.listen(port, () =>{
    console.log(`Example app listening on port ${port}`)
})