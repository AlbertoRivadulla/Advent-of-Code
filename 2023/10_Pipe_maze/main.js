const fs = require('fs');

// Different directions
const directions = {
  'N' : [ -1,  0 ],
  'S' : [  1,  0 ],
  'E' : [  0,  1 ],
  'W' : [  0, -1 ]
};

const moveInDirection = ( currentPos, dir ) => {
  let nextPos = [ 0, 0 ];
  nextPos[0] = currentPos[0] + directions[dir][0];
  nextPos[1] = currentPos[1] + directions[dir][1];
  return nextPos;
}

const checkEqualPositions = ( pos1, pos2 ) => {
  for ( let i = 0; i < pos1.length; ++i ) {
    if ( pos1[i] != pos2[i] ) {
      return false;
    }
  }
  return true;
}

// Change in direction from each pipe
/*
  | is a vertical pipe connecting north and south.
  - is a horizontal pipe connecting east and west.
  L is a 90-degree bend connecting north and east.
  J is a 90-degree bend connecting north and west.
  7 is a 90-degree bend connecting south and west.
  F is a 90-degree bend connecting south and east.
*/
const changeDirs = {
  '|' : { 'N' : 'N', 'S' : 'S' },
  '-' : { 'E' : 'E', 'W' : 'W' },
  'L' : { 'S' : 'E', 'W' : 'N' },
  'J' : { 'S' : 'W', 'E' : 'N' },
  '7' : { 'E' : 'S', 'N' : 'W' },
  'F' : { 'N' : 'E', 'W' : 'S' },
  'S' : { 'N' : 'N', 'S' : 'S', 'E' : 'E', 'W' : 'W' }
};


// Read the map
let data = fs.readFileSync('input.txt', 'utf-8').trim().split('\n');
// Parse the map into an array of arrays
let map = [];
for ( let line of data ) {
  let thisLine = [];
  for ( let char of line ) {
    thisLine.push( char );
  }
  map.push( thisLine );
}


////////////////////////////////////////////////////////////////////////////////
// First part
////////////////////////////////////////////////////////////////////////////////

let startTime = Date.now();

// Parse the map and find the S
let startingPos;
for ( let i = 0; i < map.length; ++i ) {
  for ( let j = 0; j < map[i].length; ++j ) {
    if ( map[i][j] === 'S' ) {
      startingPos = [ i, j ];
    }
  }
}

// Find what directions I can start in
let startingDirs = [];
for ( let dir in directions ) {
  let nextPos = moveInDirection( startingPos, dir );
  if ( nextPos[0] >= 0 && nextPos[1] >= 0 && nextPos[0] < map.length && nextPos[1] < map[0].length) {
    // Check if I can reach the starting position from moving in the allowed 
    // directions from that next position
    let nextDirections = changeDirs[map[nextPos[0]][nextPos[1]]];
    for ( let key in nextDirections ) {
      let nextNextPos = moveInDirection( nextPos, nextDirections[key] );
      if ( checkEqualPositions( nextNextPos, startingPos ) ) {
        startingDirs.push( dir );
      }
    }
  }
}

// Move along the map in both directions
// let distancesLeft  = [];
// let distancesRight = [];
let currPosLeft    = startingPos.slice();
let currPosRight   = startingPos.slice();
let dirLeft  = startingDirs[0];
let dirRight = startingDirs[1];
let longestDistLeft  = 0;
let longestDistRight = 0;
do {
  // Move to the left
  currPosLeft = moveInDirection( currPosLeft, dirLeft );
  dirLeft = changeDirs[map[currPosLeft[0]][currPosLeft[1]]][dirLeft];
  longestDistLeft += 1;

  // Move to the right
  currPosRight = moveInDirection( currPosRight, dirRight );
  dirRight = changeDirs[map[currPosRight[0]][currPosRight[1]]][dirRight];
  longestDistRight += 1;
} while ( !checkEqualPositions( currPosLeft, currPosRight ) )


console.log("\n\n--------------\nFirst part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Longest distance on the loop: ' + longestDistLeft);


////////////////////////////////////////////////////////////////////////////////
// Second part
////////////////////////////////////////////////////////////////////////////////

startTime = Date.now();

// Move until I come back to the starting point (doesn't matter which direction)
let currPos = startingPos.slice();
let currDir = startingDirs[0];
// let pointsInLoop = [];

// This denotes what each cell of the map is
//  0 -> ground or unused pipes
//  1 -> pipes in the loop
let mapFlags = new Array(map.length).fill(0).map(() => new Array(map[0].length).fill(0));

// Find points in the loop
while (true) {
  // Mark this point as a pipe in the loop
  mapFlags[currPos[0]][currPos[1]] = 1;
  // Move along the path
  currPos = moveInDirection( currPos, currDir );
  if ( checkEqualPositions( currPos, startingPos ) ) {
    break;
  }
  currDir = changeDirs[map[currPos[0]][currPos[1]]][currDir];
}

// Find ground points
let groundPoints = [];
for ( let i = 0; i < map.length; ++i ) {
  for ( let j = 0; j < map[i].length; ++j ) {
    if ( mapFlags[i][j] === 0 ) {
      groundPoints.push( [i, j] );
    }
  }
}

// Count the ground points that are completely enclosed by the loop
let nrEnclosedPoints = 0;
for ( let groundPt of groundPoints ) {
  // Find pipes in the loop to its left and to its right
  let pipesLeft  = [];
  let pipesRight = [];
  for ( let j = 0; j < map[0].length; ++j ) {
    if ( mapFlags[groundPt[0]][j] === 1 ) {
      if ( j < groundPt[1] ) {
        pipesLeft.push( [ groundPt[0], j ] );
      } else {
        pipesRight.push( [ groundPt[0], j ] );
      }
    }
  }

  // In order for the point to be enclosed, it needs to have both pipes to the 
  // left and to the right
  if ( pipesLeft.length > 0 && pipesRight.length > 0 ) {
    // Count of pipes to the left, with corners being +0.5 or -0.5
    let count = 0;
    for ( let pipePos of pipesLeft ) {
      let pipe = map[pipePos[0]][pipePos[1]];
      // console.log(pipePos);
      // console.log(pipe);
      if ( pipe === '|' ) {
        count += 1;
      } else if ( pipe === 'L' || pipe === '7' ) {
        count += 0.5;
      } else if ( pipe === 'J' || pipe === 'F' ) {
        count -= 0.5;
      }
    }

    count = Math.abs( count );
    if ( count % 2 === 1 ) {
      console.log('Enclosed: ' + groundPt );
      nrEnclosedPoints += 1;
    }
  }
}


console.log("\n\n--------------\nSecond part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Number of enclosed points: ' + nrEnclosedPoints);
