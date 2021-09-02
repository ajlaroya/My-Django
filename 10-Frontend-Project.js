// adds numbers to buttons as a visual reference/aid
// for (slot in $("button")) {
//   $("button").eq(slot).text(slot);
// }

// prompt for P1 and P2 name
var p1 = prompt("Player 1: Please enter your name. You will be red.");
var p1Colour = '#eb4034';

var p2 = prompt("Player 2: Please enter your name. You will be yellow.");
var p2Colour = '#ffea00';

// game conditions
var game_on = true;
var table = $('table tr');

// win check console.log();
function logWin(rowNum,colNum){
  console.log('Winner starting at this row, col');
  console.log(rowNum);
  console.log(colNum);
}

// change colour of specific column and row index of a table
function changeColour(rowIndex,colIndex,colour){
  return table.eq(rowIndex).find('td').eq(colIndex).find('button').css('background-color',colour);
}

// return colour for later use
function returnColour(rowIndex,colIndex){
  return table.eq(rowIndex).find('td').eq(colIndex).find('button').css('background-color');
}

// take column index and return bottom row
function getBottom(colIndex){
  var colourReport = returnColour(5, colIndex);
  for (var row = 5; row > -1; row--) {
    colourReport = returnColour(row,colIndex);
    if (colourReport === "rgb(255, 255, 255)") {
      return row;
    }
  }
}

// connect four check
function connectFour(one,two,three,four){
  return (one == two && one == three && one == four && one !== "rgb(255, 255, 255)" & one !== undefined);
}

// Check for Horizontal Wins
function horizontalWinCheck() {
  for (var row = 0; row < 6; row++) {
    for (var col = 0; col < 4; col++) {
      if (connectFour(returnColour(row,col), returnColour(row,col+1) ,returnColour(row,col+2), returnColour(row,col+3))) {
        console.log('horiz');
        logWin(row,col);
        return true;
      }else {
        continue;
      }
    }
  }
}

// Check for Vertical Wins
function verticalWinCheck() {
  for (var col = 0; col < 7; col++) {
    for (var row = 0; row < 3; row++) {
      if (connectFour(returnColour(row,col), returnColour(row+1,col) ,returnColour(row+2,col), returnColour(row+3,col))) {
        console.log('vertical');
        logWin(row,col);
        return true;
      }else {
        continue;
      }
    }
  }
}

// Check for Diagonal Wins
function diagonalWinCheck() {
  for (var col = 0; col < 5; col++) {
    for (var row = 0; row < 7; row++) {
      if (connectFour(returnColour(row,col), returnColour(row+1,col+1) ,returnColour(row+2,col+2), returnColour(row+3,col+3))) {
        console.log('diag');
        logWin(row,col);
        return true;
      }else if (connectFour(returnColour(row,col), returnColour(row-1,col+1) ,returnColour(row-2,col+2), returnColour(row-3,col+3))) {
        console.log('diag');
        logWin(row,col);
        return true;
      }else {
        continue;
      }
    }
  }
}

// starts with player 1
var currentPlayer = 1;
var currentName = p1;
var currentColour = p1Colour;

// game logic
$('#status').text(p1+" it is your turn, pick a column to drop in!");

$('.board button').on('click',function(){
  var col = $(this).closest('td').index();
  var bottom = getBottom(col);
  changeColour(bottom, col, currentColour);

  if (horizontalWinCheck() || verticalWinCheck() || diagonalWinCheck()) {
    $('h1').text(currentName+" has won! Refresh browser to play again.");
    // $('#instruct').fadeOut('fast'); slim jquery = no animations
    // $('#status').fadeOut('fast');
  }

  currentPlayer = currentPlayer * -1 // no win or tie

  if (currentPlayer === 1){
    currentName = p1;
    $('#status').text(currentName+" it is your turn.");
    currentColour = p1Colour;
  } else {
    currentName = p2;
    $('#status').text(currentName+" it is your turn.");
    currentColour = p2Colour;
  }
})

// REDUNDANT CODE BY YOURS TRULY:

// var toggle = false;
// number columns into arrays? maybe nested array?
// var c1 = [0,7,14,21,28,35];
// var c2 = [1,8,15,22,29,36];
// var c3 = [2,9,16,23,30,37];
// var c4 = [3,10,17,24,31,38];
// var c5 = [4,11,18,25,32,39];
// var c6 = [5,12,19,26,33,40];
// var c7 = [6,13,20,27,34,41];
// var c = [[0,7,14,21,28,35],
//         [1,8,15,22,29,36],
//         [2,9,16,23,30,37],
//         [3,10,17,24,31,38],
//         [4,11,18,25,32,39],
//         [5,12,19,26,33,40],
//         [6,13,20,27,34,41]];
//
// // click column > change color of bottom column
// for (var i = 0; i < c1.length; i++) {
//   slots.eq(c1[i]).click(function(){
//     if (toggle == false) {
//       slots.eq(c1[c1.length-1]).css("background-color","yellow");
//       toggle = true;
//       c1.pop();
//     }
//     else {
//       slots.eq(c1[c1.length-1]).css("background-color","red");
//       toggle = false;
//       c1.pop();
//     }
//   })
// }
//
// for (var i = 0; i < c.length; i++) {
//   for (var j = 0; j < c[i].length; j++) {
//     console.log(c[i][j]);
//
//     slots.eq(c[i][j]).click(function(){
//       if (toggle == false) {
//         slots.eq(c[i][c[i].length-1]).css("background-color","yellow");
//         toggle = true;
//         c[i].pop();
//       }
//       else {
//         slots.eq(c1[c1.length-1]).css("background-color","red");
//         toggle = false;
//         c.pop();
//       }
//     })
//   }
// }
