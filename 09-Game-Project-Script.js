// Grabs all table cells
var cells = document.querySelectorAll("td");

// Adds event listeners
for (var cell of cells) {
  cell.addEventListener('click', marker)
}

// Function to change markers
// With the help of: https://stackoverflow.com/questions/46341171/how-to-addeventlistener-to-table-cells
function marker() {
  if (this.textContent === 'X') {
    this.innerHTML = "O";
  } else if (this.textContent === 'O') {
    this.innerHTML = " ";
  } else {
    this.innerHTML = "X";
  }
}

// Restart game button
var restart = document.querySelector("#restart");
restart.addEventListener('click', function(){
  for (var cell of cells) {
    cell.innerHTML = " ";
  }
})
