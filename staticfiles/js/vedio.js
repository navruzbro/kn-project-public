
//VEDIO controls//

document.addEventListener('DOMContentLoaded', function () {
    var video = document.querySelector('#film-vedio');
    var playPauseButton = document.getElementById('play-pause-button');
    var muteButton = document.getElementById('mute-button');
    var volumeControl = document.getElementById('volume');

    playPauseButton.addEventListener('click', function () {
      if (video.paused || video.ended) {
        video.play();
        playPauseButton.textContent = 'To\'xtatish';
      } else {
        video.pause();
        playPauseButton.textContent = 'O\'ynatish';
      }
    });

    muteButton.addEventListener('click', function () {
      if (video.muted) {
        video.muted = false;
        
        muteButton.textContent = 'Ovozsiz';
      } else {
        video.muted = true;
        muteButton.textContent = 'Ovozli';
      }
    });

    volumeControl.addEventListener('input', function () {
      video.volume = volumeControl.value;
    });
  });

  //VEDIO sifatini o'zgartirish nastroykalari//
  var video = document.getElementById("#film-vedio");

   function changeQuality(sourceId) {
      var selectedSource = document.getElementById(sourceId);
      
      if (selectedSource) {
         video.src = selectedSource.src;
         video.load();
         video.play();
      }
   }

   var video = document.querySelector('#film-vedio');
   var progressBar = document.getElementById('progressBar');
   var volumeControl = document.getElementById('volumeControl');
   var currentTimeDisplay = document.getElementById('currentTime');



//FILM TIZER controls
//VEDIO controls//

document.addEventListener('DOMContentLoaded', function () {
  var video = document.querySelector('#film-tizer');
  var muteButton = document.getElementById('mute-button-tizer');


  muteButton.addEventListener('click', function () {
    if (video.muted) {
      video.muted = false;
      
      
    } else {
      video.muted = true;
  
    }
  });

});
