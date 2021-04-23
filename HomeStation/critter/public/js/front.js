'use strict'

/*Fade in function used to fade between pages*/
function fadeInPage() {
  if (!window.AnimationEvent) { return; }
  var fader = document.getElementById('fader');
  fader.setAttribute('class', 'fade-out');
}

/*Animation Fade Out Event*/
document.addEventListener('DOMContentLoaded', function() {
  if (!window.AnimationEvent) { return; }
  var anchors = document.getElementsByTagName('a');
    
    /*Look at all anchors*/
    for (var idx=0; idx<anchors.length; idx+=1) {
      /*Disregard all external links and links to anchors on the same page */
      if (anchors[idx].hostname !== window.location.hostname || anchors[idx].pathname === window.location.pathname) 
      { continue; }

    /*For all internal links wait until animation is finished*/
    anchors[idx].addEventListener('click', function(event) {
      var fader = document.getElementById('fader'),
          anchor = event.currentTarget;
      
      var listener = function() {
          window.location = anchor.href;
          fader.removeEventListener('animationend', listener);
      };
      fader.addEventListener('animationend', listener);
      
      event.preventDefault();

      /*Initiate fade in*/
      fader.setAttribute('class', 'fade-in');
    });
  }
});

/*Unfade cached page*/
window.addEventListener('pageshow', function (event) {
  if (!event.persisted) {
    return;
  }
  var fader = document.getElementById('fader')
  fader.removeAttribute('class', 'fade-in')
  fader.setAttribute('class', 'fade-out')
});

/*===================================*/
/*    Log directory loop settings    */
/*===================================*/
let fileNames = []
let dirPath = '/critter/logs'
var arr = {}

//Formats for current date
var q = new Date()
var mm = q.getMonth() + 1
var dd = q.getDate()
var yyyy = q.getFullYear()
if(mm < 10) {
  mm = '0' + mm
}
if(dd < 10) {
  dd = '0' + dd
}
var today = mm + '-' + dd + '-' + yyyy
console.log('Todays date: ' + today)

//AJAX call to server
function ajaxCall(callback) {
  $.ajax({
    type: 'GET',
    url: dirPath,
    dataType: 'json',
    success: callback
  })
}
ajaxCall(result => {
  console.log('Data received: ' + JSON.stringify(result))
  //Store object in localstorage for addressing later
  localStorage.setObject(result.Entry, )
  //Call function to add to tab menus
  DataEntry(result)
})

//Function takes in JSON data string and displays as log in tabs
function DataEntry(data) {
  //If log date is today, put in today panel
  if (today == JSON.stringify(data.Date).replace(/['"]+/g, '')) {
    var ul = document.getElementById('today-logs')
    var li = document.createElement('li')
    ul.appendChild(li)
    li.innerHTML = li.innerHTML + data.Entry
  }
  //Else if log date is older than today, put in older panel
  else if (today > JSON.stringify(data.Date).replace(/['"]+/g, '')) {
    var ul = document.getElementById('older-logs')
    var li = document.createElement('li')
    ul.appendChild(li)
    li.innerHTML = li.innerHTML + data.Entry
  }
  
  //If a log file is clicked, then loop through JSON and display info
  var ultoday = document.getElementById('today-logs')
  ultoday.addEventListener('click', function(event) {
    for (var key in data) {
      if(key == 'Entry') {
      }
      //Convert time from millitary to default using moment
      else if(key == 'Time') {
        var p = document.getElementById(key)
        p.innerHTML = moment(data.Time, 'HH::mm').format('h:mm A')
        //Have text fade in from white
        p.style.color = "#e65656";
      }
      else {
        var p = document.getElementById(key)
        p.innerHTML = data[key]
        p.style.color = "#e65656";
      }
    }
  })

  //If a log file is clicked, then loop through JSON and display info
  var ulolder = document.getElementById('older-logs')
  ulolder.addEventListener('click', function(event) {
    for (var key in data) {
      if(key == 'Entry') {
      }
      //Convert time from millitary to default using moment
      else if(key == 'Time') {
        var p = document.getElementById(key)
        p.innerHTML = moment(data.Time, 'HH::mm').format('h:mm A')
        //Have text fade in from white
        p.style.color = "#e65656";
      }
      else {
        var p = document.getElementById(key)
        p.innerHTML = data[key]
        p.style.color = "#e65656";
      }
    }
  })
}

//Set two functions to insert objects into browser localstorage
//Using a key,value pair
Storage.prototype.setObject = function(key, value) {
  this.setItem(key, JSON.stringify(value));
}

Storage.prototype.getObject = function(key) {
  var value = this.getItem(key);
  return value && JSON.parse(value);
}