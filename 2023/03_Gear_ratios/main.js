const fs = require('fs');


// Function to check if a character is a digit
function isDigit( char ) {
  return ( char >= '0' && char <= '9' );
}

// Function to check if a neighbor is valid
const isValidNeighbor = (x, y, lengthX, lengthY) => {
  return x >= 0 && y >= 0 && x < lengthX && y < lengthY;
}


// Read the data
let data = fs.readFileSync('input.txt', 'utf-8').trim().split('\n');

////////////////////////////////////////////////////////////////////////////////
// First part
////////////////////////////////////////////////////////////////////////////////

let startTime = Date.now();

const parseLine = (data, lineInd) => {
  let thisSum = 0;

  // Horizontal and vertical lengths of the data array
  let lengthX = data[lineInd].length;
  let lengthY = data.length;

  // Move along the line
  let i1 = 0;
  let i2 = 0;
  while ( i1 < data[lineInd].length ) {
    // Move on the line until a number is found
    while ( !isDigit(data[lineInd][i1]) && i1 < data[lineInd].length ) 
      i1++;
    // When a number is found, move the second index to find its end
    i2 = i1 + 1;
    while ( isDigit(data[lineInd][i2]) )
      i2++;

    // Find all the neighbors of the number
    let neighbors = [];
    // Neighbors above and below
    for ( let x = i1-1; x <= i2; ++x ) {
      for ( let y = lineInd - 1; y <= lineInd + 1; y += 2 ) {
        if ( isValidNeighbor( x, y, lengthX, lengthY ) )
          neighbors.push( [ x, y ] );
      }
    }
    // Left and right neighbors
    if ( isValidNeighbor( i1-1, lineInd, lengthX, lengthY ) )
      neighbors.push( [ i1-1, lineInd ] );
    if ( isValidNeighbor( i2, lineInd, lengthX, lengthY ))
      neighbors.push( [ i2, lineInd ] );

    // Check if this is a part number (it has to be adjacent to a symbol)
    for ( const neigh of neighbors ) {
      let neighChar = data[neigh[1]][neigh[0]];
      if ( !(neighChar === '.') && !isDigit(neighChar) ) {
        thisSum += Number( data[lineInd].slice(i1, i2) );
        // console.log("Part number: " + data[lineInd].slice(i1, i2));
        break;
      }
    }

    i1 = i2;
    i1++;
  }

  return thisSum;
}


let sumParts = 0;
for (let i = 0; i < data.length; ++i) {
  sumParts += parseLine( data, i );
}

console.log("\n\n--------------\nFirst part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log("Sum of all parts: " + sumParts);


////////////////////////////////////////////////////////////////////////////////
// Second part
////////////////////////////////////////////////////////////////////////////////

startTime = Date.now();

const parseLineForGears = (data, lineInd, gears) => {
  // Horizontal and vertical lengths of the data array
  let lengthX = data[lineInd].length;
  let lengthY = data.length;

  // Move along the line
  let i1 = 0;
  let i2 = 0;
  while ( i1 < data[lineInd].length ) {
    // Move on the line until a number is found
    while ( !isDigit(data[lineInd][i1]) && i1 < data[lineInd].length ) 
      i1++;
    // When a number is found, move the second index to find its end
    i2 = i1 + 1;
    while ( isDigit(data[lineInd][i2]) )
      i2++;

    // Find all the neighbors of the number
    let neighbors = [];
    // Neighbors above and below
    for ( let x = i1-1; x <= i2; ++x ) {
      for ( let y = lineInd - 1; y <= lineInd + 1; y += 2 ) {
        if ( isValidNeighbor( x, y, lengthX, lengthY ) )
          neighbors.push( [ x, y ] );
      }
    }
    // Left and right neighbors
    if ( isValidNeighbor( i1-1, lineInd, lengthX, lengthY ) )
      neighbors.push( [ i1-1, lineInd ] );
    if ( isValidNeighbor( i2, lineInd, lengthX, lengthY ))
      neighbors.push( [ i2, lineInd ] );

    // Look for a gear in its neighbors
    for ( const neigh of neighbors ) {
      let neighChar = data[neigh[1]][neigh[0]];
      if ( neighChar === '*' ) {
        let coordsNr = neigh[0] + neigh[1] * lengthX;
        if ( gears[coordsNr] )
          gears[coordsNr].push( Number(data[lineInd].slice(i1, i2)) );
        else
          gears[coordsNr] = [ Number(data[lineInd].slice(i1, i2)) ];
      }
    }

    i1 = i2;
    i1++;
  }
}


// Find all gears in the map
let gears = {};
for (let i = 0; i < data.length; ++i) {
  parseLineForGears( data, i, gears );
}

// Sum the ratios of the valid gears
let sumGearRatios = 0;
for ( const key in gears ) {
  if ( gears[key].length === 2 ) {
    sumGearRatios += gears[key][0] * gears[key][1];
  }
}

console.log("\n\n--------------\nSecond part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Sum of gear ratios: ' + sumGearRatios);
