var slots = $("button");

// visual aid
for (slot in slots) {
  slots.eq(slot).text(slot);
  // slots.eq(slot).click(function(){
  //   $(this).css("background-color","yellow");
  // })
}

// prompt for P1 and P2 name

// number columns into arrays?
var c1 = [0,7,14,21,28,35];

slots.eq(0).click(function(){
  slots.eq(c1[c1.length-1]).css("background-color","yellow");
  c1.pop();
})


// click column > change color of last column

// toggle color yellow/red after click

// win case scenario checks
