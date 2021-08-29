// var tableCell = document.querySelectorAll("td");
//
// for (var i = 0; i < tableCell.length; i++) {
//   tableCell[i].addEventListener("click",function(){
//     for (var x = 0; i < tableCell.length; x++) {
//       console.log(x);
//       tableCell[x].textContent = ' ';
//     }
//   })
// }
//
// // tableCell.addEventListener("click",function(){
// //   tableCell.textContent = ' ';
// // })

var cells = document.querySelectorAll("td");

for (var cell of cells) {
  cell.addEventListener('click', marker)
}

function marker() {
  if (this.textContent === 'X') {
    this.innerHTML = "O";
  } else if (this.textContent === 'O') {
    this.innerHTML = " ";
  } else {
    this.innerHTML = "X";
  }
}
