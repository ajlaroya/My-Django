function commentReplyToggle(parent_id) {
  const row = document.getElementById(parent_id);
  if (row.classList.contains('is-hidden')) {
    row.classList.remove('is-hidden');
  } else {
    row.classList.add('is-hidden');
  }
}

function showNotifications() {
  const container = document.getElementById('notification-container');
  if (container.classList.contains('is-hidden')) {
    container.classList.remove('is-hidden');
  } else {
    container.classList.add('is-hidden')
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Grabs CSRF token and sends AJAX request, redirects
function removeNotification(removeNotificationURL, redirectURL) {
  var xmlhttp = new XMLHttpRequest();
  const csrftoken = getCookie('csrftoken');
  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == XMLHttpRequest.DONE) {
      if (xmlhttp.status == 200) {
        window.location.replace(redirectURL);
      }
      else {
        alert('There was an error.');
      }
    }
  };
  xmlhttp.open("DELETE", removeNotificationURL, true);
  xmlhttp.setRequestHeader("X-CSRFToken", csrftoken)
  xmlhttp.send();
}

function shareToggle(parent_id) {
  const row = document.getElementById(parent_id);
  if (row.classList.contains('is-hidden')) {
    row.classList.remove('is-hidden');
  } else {
    row.classList.add('is-hidden');
  }
}

// Dynamically finds tags and links them to explore page!
function formatTags() {
  var elements = document.getElementsByClassName('post-body');
  for (let i = 0; i < elements.length; i++) {
    let bodyText = elements[i].children[0].innerText;
    let words = bodyText.split(' ');
    for (let j = 0; j < words.length; j++) {
      if (words[j][0] === '#') {
        let replacedText = bodyText.replace(/\s\#(.*?)(\s|$)/g,
        ` <a href="/posts/explore?query=${words[j].substring(1)}">${words[j]}</a>`);
        elements[i].innerHTML = replacedText
      }
    }
  }
}

formatTags();

function dropdown() {
  document.querySelectorAll('.dropdown').forEach(item => {
      item.addEventListener('click', function(event) {
          event.stopPropagation();
          item.classList.toggle('is-active');
      });
  });
}

dropdown()

// Plume logo animation
// var textWrapper = document.querySelector('.ml6 .letters');
// textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");
//
// anime.timeline({loop: true})
//   .add({
//     targets: '.ml6 .letter',
//     translateY: ["0.40em", 0],
//     translateZ: 0,
//     duration: 1500,
//     delay: (el, i) => 75 * i
//   })

// Staggering animation
// function fitElementToParent(el, padding) {
//   var timeout = null;
//   function resize() {
//     if (timeout) clearTimeout(timeout);
//     anime.set(el, {scale: 1});
//     var pad = padding || 0;
//     var parentEl = el.parentNode;
//     var elOffsetWidth = el.offsetWidth - pad;
//     var parentOffsetWidth = parentEl.offsetWidth;
//     var ratio = parentOffsetWidth / elOffsetWidth;
//     timeout = setTimeout(anime.set(el, {scale: ratio}), 10);
//   }
//   resize();
//   window.addEventListener('resize', resize);
// }
//
// var advancedStaggeringAnimation = (function() {
//
//   var staggerVisualizerEl = document.querySelector('.stagger-visualizer');
//   var dotsWrapperEl = staggerVisualizerEl.querySelector('.dots-wrapper');
//   var dotsFragment = document.createDocumentFragment();
//   var grid = [20, 10];
//   var cell = 55;
//   var numberOfElements = grid[0] * grid[1];
//   var animation;
//   var paused = true;
//
//   fitElementToParent(staggerVisualizerEl, 0);
//
//   for (var i = 0; i < numberOfElements; i++) {
//     var dotEl = document.createElement('div');
//     dotEl.classList.add('dot');
//     dotsFragment.appendChild(dotEl);
//   }
//
//   dotsWrapperEl.appendChild(dotsFragment);
//
//   var index = anime.random(0, numberOfElements-1);
//   var nextIndex = 0;
//
//   anime.set('.stagger-visualizer .cursor', {
//     translateX: anime.stagger(-cell, {grid: grid, from: index, axis: 'x'}),
//     translateY: anime.stagger(-cell, {grid: grid, from: index, axis: 'y'}),
//     translateZ: 0,
//     scale: 1.5,
//   });
//
//   function play() {
//
//     paused = false;
//     if (animation) animation.pause();
//
//     nextIndex = anime.random(0, numberOfElements-1);
//
//     animation = anime.timeline({
//       easing: 'easeInOutQuad',
//       complete: play
//     })
//     .add({
//       targets: '.stagger-visualizer .cursor',
//       keyframes: [
//         { scale: .75, duration: 120},
//         { scale: 2.5, duration: 220},
//         { scale: 1.5, duration: 450},
//       ],
//       duration: 300
//     })
//     .add({
//       targets: '.stagger-visualizer .dot',
//       keyframes: [
//         {
//           translateX: anime.stagger('-2px', {grid: grid, from: index, axis: 'x'}),
//           translateY: anime.stagger('-2px', {grid: grid, from: index, axis: 'y'}),
//           duration: 100
//         }, {
//           translateX: anime.stagger('4px', {grid: grid, from: index, axis: 'x'}),
//           translateY: anime.stagger('4px', {grid: grid, from: index, axis: 'y'}),
//           scale: anime.stagger([2.6, 1], {grid: grid, from: index}),
//           duration: 225
//         }, {
//           translateX: 0,
//           translateY: 0,
//           scale: 1,
//           duration: 1200,
//         }
//       ],
//       delay: anime.stagger(80, {grid: grid, from: index})
//     }, 30)
//     .add({
//       targets: '.stagger-visualizer .cursor',
//       translateX: { value: anime.stagger(-cell, {grid: grid, from: nextIndex, axis: 'x'}) },
//       translateY: { value: anime.stagger(-cell, {grid: grid, from: nextIndex, axis: 'y'}) },
//       scale: 1.5,
//       easing: 'cubicBezier(.075, .2, .165, 1)'
//     }, '-=800')
//
//     index = nextIndex;
//
//   }
//
//   play();
//
// })();


// Copyright start
// © Code by T.RICKS, https://www.tricksdesign.com/
// You have the license to use this code in your projects but not redistribute it to others

// Find all text with .tricks class and break each letter into a span
var tricksWord = document.getElementsByClassName("tricks");
for (var i = 0; i < tricksWord.length; i++) {
  var wordWrap = tricksWord.item(i);
  wordWrap.innerHTML = wordWrap.innerHTML.replace(/(^|<\/?[^>]+>|\s+)([^\s<]+)/g, '$1<span class="tricksword">$2</span>');
}

var tricksLetter = document.getElementsByClassName("tricksword");
for (var i = 0; i < tricksLetter.length; i++) {
  var letterWrap = tricksLetter.item(i);
  letterWrap.innerHTML = letterWrap.textContent.replace(/\S/g, "<span class='letter'>$&</span>");
}

// Copyright end

// Slide In Animation
var slideIn = anime.timeline({
  loop: false,
  autoplay: false,
});
slideIn
  .add({
    targets: '.slide-in .letter',
    opacity: [0, 1],
    easing: "easeInOutQuad",
    duration: 2250,
    delay: (el, i) => 150 * (i + 1)
  }).add({
    targets: '.slide-in',
    opacity: 0,
    duration: 1000,
    easing: "easeOutExpo",
    delay: 1000
  });


// Slide Up Animation
var slideUp = anime.timeline({
  loop: false,
  autoplay: false,
});
slideUp
  .add({
    targets: '.slide-up .letter',
    translateY: ["1.1em", 0],
    opacity: [0, 1],
    translateZ: 0,
    duration: 750,
    delay: (el, i) => 50 * i
  })


// Fade Up Animation
var fadeUp = anime.timeline({
  loop: false,
  autoplay: false,
});
fadeUp
  .add({
    targets: '.fade-up .letter',
    translateY: [100, 0],
    translateZ: 0,
    opacity: [0, 1],
    easing: "easeOutExpo",
    duration: 1400,
    delay: (el, i) => 300 + 30 * i
  });

// Fade Up Splits Animation
var fadeUpSplit = anime.timeline({
  loop: false,
  autoplay: false,
});
fadeUpSplit
  .add({
    targets: '.fade-up-split .tricksword',
    translateY: [100, 0],
    translateZ: 0,
    opacity: [0, 1],
    rotateZ: [45, 0],
    easing: "easeOutExpo",
    duration: 1400,
    delay: (el, i) => 300 + 30 * i
  });

// Fade Up Cards Animation
var fadeUpCards = anime.timeline({
  loop: false,
  autoplay: false,
});
fadeUpCards
  .add({
    targets: '.fade-up-cards',
    translateX: [100, 0],
    translateZ: 0,
    opacity: [0, 1],
    easing: "easeOutExpo",
    duration: 3000,
    delay: (el, i) => 200 + 200 * i
  });


// Rotate In Animation
var rotateIn = anime.timeline({
  loop: false,
  autoplay: false,
});
rotateIn
  .add({
    targets: '.rotate-in .tricksword',
    translateY: ["1.1em", 0],
    translateX: ["0.55em", 0],
    translateZ: 0,
    rotateZ: [45, 0],
    duration: 2000,
    opacity: [0, 1],
    easing: "easeOutExpo",
  });


// Pop In Animation
var popIn = anime.timeline({
  loop: false,
  autoplay: false,
});
popIn
  .add({
    targets: '.pop-in .letter',
    scale: [0, 1],
    duration: 1500,
    elasticity: 600,
    delay: (el, i) => 45 * (i + 1)
  });


// Play your animation with these
slideUp.play();
slideIn.play();
popIn.play();


// Wait before playing animation
setTimeout(() => {
  // Put the play below this line
}, 800);


// Play animaton when something is clicked
$(".your-button-class").click(function() {
  // Put the play below this line
});


// Play animaton when hovered in
$(".your-button-class").mouseenter(function() {
  // Put the play below this line
});


// Play animation when scrolled into view
$('.hero--gallery').on('inview', function(event, isInView) {
  if (isInView) {
    // Put the play below this line
        fadeUp.play();
        popIn.play();
        slideIn.play();
        // fadeUp.restart();
  } else {}
});

// Play animation when scrolled into view
$('.c-split').on('inview', function(event, isInView) {
  if (isInView) {
    // Put the play below this line
      fadeUpSplit.play();
  } else {}
});

// Play animation when scrolled into view
$('.c-two-col--freeform').on('inview', function(event, isInView) {
if (isInView) {
// Put the play below this line
fadeUpCards.play();
} else {}
});
