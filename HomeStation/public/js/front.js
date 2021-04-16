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

/*
Promise.all([
  fetch('/Logs/4-12-2021_1400.txt').then(x => x.text())
]).then(([sampleResp]) => {
  console.log(sampleResp);
});
*/

/*===================================*/
/*    Log directory loop settings    */
/*===================================*/
let str = '<ul>'
let fileNames = []
var socket = io()

socket.on('initialize array', function(init_fileNames) {
  fileNames = init_fileNames
})
  .on('change', function(data) {
    fileNames.push(data)
    console.log(fileNames)
})

str += '</ul>'