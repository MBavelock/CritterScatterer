/*--------------------------------------*/
/*               Imports                */
/*--------------------------------------*/
//Filesystem imports
const fs = require('fs')

//Server Setup
const port = 8080
const express = require('express')
const { dir } = require('console')
const { query } = require('express')
const { userInfo } = require('os')
const app     = express()
var server    = require('http').createServer(app)

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
/*        Info for database files       */
/*--------------------------------------*/
let dirPath = '/home/pi/critter/logs/'

app.get(dirPath, function(req, res){
  let fileNames = fs.readdirSync(dirPath)
  //Loop through each file backwards and create objects to send
  fileNames.slice().reverse().forEach((file) => {
    //Read file line by line
    fs.readFile(dirPath + file, 'utf8', function (err, data) {
      if (err) throw err

      Entry = file.slice(0, -4) //Remove .txt extension

      let obj = { Entry }
      let splitted = data.toString().split('\n')  //Split line by line

      //Split by each space and store into object
      for (let i = 0; i < splitted.length; i++) {
        let splitLine = splitted[i].split(' ')
        obj[splitLine[0]] = splitLine[1].trim()
      }
      var json = JSON.stringify(obj)
      //Send the data to client
      console.log('\nObj sent:' + json)
      res.send(json)
    })
  })
})

//Listen on port 8080
server.listen(port, '192.168.1.89', () => {
  console.log('Server listening on Port 8080');
})
