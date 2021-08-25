var firstName = prompt("First name: ");
var secondName = prompt("Second name: ");
var age = prompt("Age: ");
var height = prompt("Height (cm): ");
var petName = prompt("Pet name: ");

alert("Thank you for the information!")

if ((firstName[0] === secondName[0]) && (20 > age < 30) && (height >= 170) &&
(petName[petName.length - 1] === "y")) {
  console.log("Hello there agent " + firstName+ ", we've been waiting for you...");
}
else {
  console.log('Carry on...');
}
