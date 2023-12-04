const fs = require('fs');



// Read the data
let data = fs.readFileSync('input.txt', 'utf-8').trim().split('\n');

////////////////////////////////////////////////////////////////////////////////
// First part
////////////////////////////////////////////////////////////////////////////////

let startTime = Date.now();

// Contents of the bag
const bagContents = {
  'red'   : 12,
  'green' : 13,
  'blue'  : 14
};

// Check if a game is valid
let isGameValid = (gameStr, bagContents) => {
  // Split the game in sets
  var sets = gameStr.split(';');

  // Iterate over the sets, and check that they are all valid
  for ( const set of sets ) {
    let matches = set.match( /[0-9]+\s[a-z]+/g );
    for ( let match of matches ) {
      match = match.split(' ');
      // If there are more cubes of this color than in the bag, this is not valid
      if ( Number(match[0]) > bagContents[match[1]] )
        return false;
    }
  }

  return true;
}

let sumValidIDs = 0;
for (const game of data) {
  // Separate the game in the ID and the actual game string
  let regexMatch = game.match( /Game\s([0-9]+):\s(.+)/ );

  // Check if it is valid, and in that case add its ID to the corresponding variable.
  if ( isGameValid(regexMatch[2], bagContents) ) {
    sumValidIDs += Number( regexMatch[1] );
  }
}


console.log("\n\n--------------\nFirst part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Sum of the valid IDs: ' + sumValidIDs);


////////////////////////////////////////////////////////////////////////////////
// Second part
////////////////////////////////////////////////////////////////////////////////

startTime = Date.now();

// Compute the power of a game
let getGamePower = (gameStr) => {

  let neededCubes = {
    'red'   : 0,
    'green' : 0,
    'blue'  : 0
  };

  // Split the game in sets
  var sets = gameStr.split(';');

  // Iterate over the sets, and check that they are all valid
  for ( const set of sets ) {
    let matches = set.match( /[0-9]+\s[a-z]+/g );
    for ( let match of matches ) {
      match = match.split(' ');

      // If this set needs more cubes than before in the bag, update it
      if ( Number(match[0]) > neededCubes[match[1]] )
        neededCubes[match[1]] = Number(match[0]);
    }
  }


  // Compute the power and return it
  let power = 1;
  for ( let color in neededCubes )
    power *= neededCubes[color];

  return power;
}

let sumGamePowers = 0;
for (const game of data) {
  // Separate the game in the ID and the actual game string
  let regexMatch = game.match( /Game\s([0-9]+):\s(.+)/ );

  // Compute the power of this game and sum it
  sumGamePowers += getGamePower( regexMatch[2] );
}


console.log("\n\n--------------\nSecond part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Sum of the game powers: ' + sumGamePowers);
