const fs = require('fs');


// Read the data
let data = fs.readFileSync('input.txt', 'utf-8').trim().split('\n');
let galaxies = [];
for ( let i = 0; i < data.length; ++i ) {
  for ( let j = 0; j < data[0].length; ++j ) {
    if ( data[i].charAt(j) === '#' ) {
      galaxies.push( [ i, j ] );
    }
  }
}


////////////////////////////////////////////////////////////////////////////////
// First part
////////////////////////////////////////////////////////////////////////////////

const findShortestDistance = ( pt1, pt2 ) => {
  let distance = 0;
  distance += Math.abs( pt1[0] - pt2[0] );
  distance += Math.abs( pt1[1] - pt2[1] );
  return distance;
}


let startTime = Date.now();

// Find the maximum x and y of the galaxies.
let maxX = 0;
let maxY = 0;
for ( let galaxy of galaxies ) {
  if ( galaxy[0] > maxX ) {
    maxX = galaxy[0];
  }
  if ( galaxy[1] > maxY ) {
    maxY = galaxy[1];
  }
}

// Find the empty rows and columns
let emptyX = [];
for ( let i = 0; i < maxX; ++i ) {
  let empty = true;
  for ( let galaxy of galaxies ) {
    if ( galaxy[0] === i ) {
      empty = false;
      break;
    }
  }
  if ( empty ) {
    emptyX.push( i );
  }
}
let emptyY = [];
for ( let j = 0; j < maxY; ++j ) {
  let empty = true;
  for ( let galaxy of galaxies ) {
    if ( galaxy[1] === j ) {
      empty = false;
      break;
    }
  }
  if ( empty ) {
    emptyY.push( j );
  }
}

// Expand the universe
for ( let thisX of emptyX ) {
  for ( let ind = 0; ind < galaxies.length; ++ind ) {
    if ( galaxies[ind][0] > thisX ) {
      galaxies[ind][0] += 1;
    }
  }
  for ( let ind = 0; ind < emptyX.length; ++ind ) {
    if ( emptyX[ind] > thisX ) {
      emptyX[ind] += 1;
    }
  }
}
for ( let thisY of emptyY ) {
  for ( let ind = 0; ind < galaxies.length; ++ind ) {
    if ( galaxies[ind][1] > thisY ) {
      galaxies[ind][1] += 1;
    }
  }
  for ( let ind = 0; ind < emptyY.length; ++ind ) {
    if ( emptyY[ind] > thisY ) {
      emptyY[ind] += 1;
    }
  }
}

// Compute the sum of the shortest distances between each pair of galaxies.
let sumShortestDistances = 0;
for ( let i = 0; i < galaxies.length; i++ ) {
  for ( let j = i + 1; j < galaxies.length; ++j ) {
    sumShortestDistances += findShortestDistance( galaxies[i], galaxies[j] );
  }
}


console.log("\n\n--------------\nFirst part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Sum of shortest distances: ' + sumShortestDistances);


////////////////////////////////////////////////////////////////////////////////
// Second part
////////////////////////////////////////////////////////////////////////////////

startTime = Date.now();

// Parse the data again
galaxies = [];
for ( let i = 0; i < data.length; ++i ) {
  for ( let j = 0; j < data[0].length; ++j ) {
    if ( data[i].charAt(j) === '#' ) {
      galaxies.push( [ i, j ] );
    }
  }
}

// Find the empty rows and columns
emptyX = [];
for ( let i = 0; i < maxX; ++i ) {
  let empty = true;
  for ( let galaxy of galaxies ) {
    if ( galaxy[0] === i ) {
      empty = false;
      break;
    }
  }
  if ( empty ) {
    emptyX.push( i );
  }
}
emptyY = [];
for ( let j = 0; j < maxY; ++j ) {
  let empty = true;
  for ( let galaxy of galaxies ) {
    if ( galaxy[1] === j ) {
      empty = false;
      break;
    }
  }
  if ( empty ) {
    emptyY.push( j );
  }
}


// Expand the universe
let nrCellsExpand = 1000000 - 1;
for ( let thisX of emptyX ) {
  for ( let ind = 0; ind < galaxies.length; ++ind ) {
    if ( galaxies[ind][0] > thisX ) {
      galaxies[ind][0] += nrCellsExpand;
    }
  }
  for ( let ind = 0; ind < emptyX.length; ++ind ) {
    if ( emptyX[ind] > thisX ) {
      emptyX[ind] += nrCellsExpand;
    }
  }
}
for ( let thisY of emptyY ) {
  for ( let ind = 0; ind < galaxies.length; ++ind ) {
    if ( galaxies[ind][1] > thisY ) {
      galaxies[ind][1] += nrCellsExpand;
    }
  }
  for ( let ind = 0; ind < emptyY.length; ++ind ) {
    if ( emptyY[ind] > thisY ) {
      emptyY[ind] += nrCellsExpand;
    }
  }
}

// Compute the sum of the shortest distances between each pair of galaxies.
sumShortestDistances = 0;
for ( let i = 0; i < galaxies.length; i++ ) {
  for ( let j = i + 1; j < galaxies.length; ++j ) {
    sumShortestDistances += findShortestDistance( galaxies[i], galaxies[j] );
  }
}



console.log("\n\n--------------\nSecond part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Sum of shortest distances: ' + sumShortestDistances);
