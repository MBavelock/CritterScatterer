/*--------------------------------------*/
/*               Imports                */
/*--------------------------------------*/
//Filesystem imports
const fs = require('fs')
const readline = require('readline')

//Server Setup
const port = 8080
const express = require('express')
const app     = express()
var server    = require('http').createServer(app)
const io      = require('socket.io')(server)

/*--------------------------------------*/
/*      Info for webpage serving        */
/*--------------------------------------*/

//Point to where static files are located
app.use(express.static('public'))
app.use('/css', express.static(__dirname + 'public/css'))
app.use('/js', express.static(__dirname + 'public/js'))
app.use('/icons', express.static(__dirname + 'public/icons'))
app.use('/images', express.static(__dirname + 'public/images'))

//For home page get index.html
app.get('', (req, res) => {
  res.sendFile(__dirname + '/views/index.html')
})
//For traveling back to home page get index.html
app.get('/index.html', (req, res) => {
  res.sendFile(__dirname + '/views/index.html')
})
//For options page get options.html
app.get('/options.html', (req, res) => {
  res.sendFile(__dirname + '/views/options.html')
})
//For events page get events.html
app.get('/events.html', (req, res) => {
  res.sendFile(__dirname + '/views/events.html')
})

/*--------------------------------------*/
/*        Info for file reading         */
/*--------------------------------------*/
let dirPath = '/critter/logs/'

let fileNames = fs.readdirSync(dirPath);
console.log('\nFileNames:')

io.on('connection', function(socket) {
  console.log('User connected!')
  socket.emit('initialize array', fileNames)
  socket.on('change', function(data) {
    socket.broadcast.emit('change', data)
    fileNames.push(data)
    console.log(fileNames)
  })
})

/*Loop through each file and create a list element
fileNames.slice().reverse().forEach((file) => {
  file = file.slice(0, -4) //Remove .txt extension
  
  str += '<li>' + file + '</li>'
  console.log('File: ', str + '\n')
})
*/



/*
try {
    let data = fs.readFileSync(dirPath + file, 'utf8');
    console.log(data)
  } catch (error) {
    console.log('Error:', error.stack);
  } 
*/

//Listen on port 8080
server.listen(port, () => {
  console.log('Server listening on Port 8080');
})