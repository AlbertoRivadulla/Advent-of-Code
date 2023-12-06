const fs = require('fs');

const getNrOfWins = ( time, distance ) => {
  // Minimum and maximum time that I need to press the button in order to win
  let sqrt = Math.sqrt( time*time - 4 * distance );
  let tPressedMin = Math.floor( ( time - sqrt ) / 2 );
  let tPressedMax = Math.floor( ( time + sqrt ) / 2 );

  if ( tPressedMin * ( time - tPressedMin ) === distance )
    tPressedMin += 1;
  if ( tPressedMax * ( time - tPressedMax ) === distance )
    tPressedMax -+ 1;

  return tPressedMax - tPressedMin;
}

// Read the data
let data = fs.readFileSync('input.txt', 'utf-8').trim().split('\n');

// Read times and distances
let times     = data[0].match( /\d+/g ).map( (x) => Number(x) );
let distances = data[1].match( /\d+/g ).map( (x) => Number(x) );

////////////////////////////////////////////////////////////////////////////////
// First part
////////////////////////////////////////////////////////////////////////////////

let startTime = Date.now();

// For each race, find the number of ways that the record can be beaten
let numberOfWins = Array(times.length).fill(0);
for ( let i = 0; i < times.length; ++i ) {
  // for ( let tPressed = 0; tPressed < times[i]; ++tPressed ) {
  //   // The velocity after releasing the button is equal to tPressed.
  //   // The distance travelled is tPressed * ( times[i] - tPressed )
  //   if ( tPressed * ( times[i] - tPressed ) > distances[i] )
  //     numberOfWins[i] += 1;
  // }

  numberOfWins[i] = getNrOfWins( times[i], distances[i] );
}

// Compute the product of the number of wins
let productNrWins = 1;
for ( const nr of numberOfWins )
  productNrWins *= nr;


console.log("\n\n--------------\nFirst part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Product of the number of wins: ' + productNrWins);


////////////////////////////////////////////////////////////////////////////////
// Second part
////////////////////////////////////////////////////////////////////////////////

startTime = Date.now();

// Read the time and distance of the only race that there is
let time = '';
for ( const timeString of data[0].match(/\d+/g) )
  time += timeString;
time = Number(time);
let distance = '';
for ( const distanceString of data[1].match(/\d+/g) )
  distance += distanceString;
distance = Number(distance);

// Compute the number of wins
// numberOfWins = 0;
// for ( let tPressed = 0; tPressed < time; ++tPressed ) {
//   // The velocity after releasing the button is equal to tPressed.
//   // The distance travelled is tPressed * ( time - tPressed )
//   if ( tPressed * ( time - tPressed ) > distance )
//     numberOfWins += 1;
// }

numberOfWins = getNrOfWins( time, distance );


console.log("\n\n--------------\nSecond part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Number of wins: ' + numberOfWins);

