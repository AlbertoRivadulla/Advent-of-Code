const fs = require('fs');

// Map of the directions to indices in the list of destination nodes
let directionsToIndices = {
  'L' : 0,
  'R' : 1
};

// Read the data
let data = fs.readFileSync('input.txt', 'utf-8').trim().split('\n');

// The first line are the instructions
let instructions = data[0];

// Parse the different nodes
let nodes = {};
for ( let line of data.slice(2) ) {
  let matches = line.match( /([A-Z0-9]+)\s=\s\(([A-Z0-9]+)\,\s([A-Z0-9]+)\)/ );

  nodes[matches[1]] = [ matches[2], matches[3] ];
}

////////////////////////////////////////////////////////////////////////////////
// First part
////////////////////////////////////////////////////////////////////////////////

let startTime = Date.now();

// Starting from AAA, move following the instructions until reaching ZZZ
let currentNode = 'AAA';
let nrSteps = 0;
// while ( currentNode != 'ZZZ' ) {
//   // Move to the next node following the instructions
//   currentNode = nodes[currentNode][directionsToIndices[instructions[nrSteps % instructions.length]]];
//
//   nrSteps += 1;
// }


console.log("\n\n--------------\nFirst part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Number of steps ' + nrSteps);


////////////////////////////////////////////////////////////////////////////////
// Second part
////////////////////////////////////////////////////////////////////////////////

const findLeastCommonMultiple = ( numbers ) => {
  let factors = {};
  let newNumbers = numbers.slice();

  for ( let num of newNumbers ) {
    let factor = 2;

    while ( num > 1 ) {
      while ( num % factor === 0 ) {
        if (!(factor in factors)) {
          factors[factor] = 1;
        }
        else {
          factors[factor] += 1;
        }

        // Divide all the numbers by this factor, if possible
        for ( let i = 0; i < newNumbers.length; ++i ) {
          if ( newNumbers[i] % factor === 0 )
            newNumbers[i] = newNumbers[i] / factor;
        }

        num /= factor;
      }
      factor += 1;
    }
  }

  let LCM = 1;
  for ( let factor in factors ) {
    LCM *= Number(factor) ** factors[factor];
  }

  return LCM;

}

startTime = Date.now();

// Find the starting nodes, those that end with A
let startNodes = [];
for ( let node in nodes ) {
  if ( node[2] === 'A' ) {
    startNodes.push( node );
  }
}

// Find the goal nodes, those that end with Z
let goalNodes = [];
for ( let node in nodes ) {
  if ( node[2] === 'Z' ) {
    goalNodes.push( node );
  }
}

// Amount of steps to go from each starting node to each of the goal nodes
let stepsToGoals = {};
// for ( let startNode of startNodes ) {
for ( let startNode of startNodes.slice(0) ) {
  stepsToGoals[startNode] = [];
  let currNode = startNode;
  let currNrSteps = 0;

  let nrInstr = instructions.length;

  let lastNrSteps = 0;

  // while ( currNode != startNode ) {
  while ( true ) {
    // Move to the next node
    currNode = nodes[currNode][directionsToIndices[instructions[currNrSteps % nrInstr]]];

    currNrSteps += 1;

    // If the current node ends with Z, save the number of steps
    if ( currNode[2] === 'Z' ) {
      if ( lastNrSteps != 0 ) {
        // This saves the number of steps to reach the goal the first time, and the 
        // periodicity afterwards.
        stepsToGoals[startNode].push( [ currNode, lastNrSteps, currNrSteps - lastNrSteps ] );
        break;
      }

      lastNrSteps = currNrSteps;
    }
  }
}

// I found that if I start at node xxA, I reach the corresponding yyZ after nrSteps.
// If it iterates for nrSteps more, the node yyZ is reached again. 
// Therefore, in order to find the minimum number of steps for all paths to be at
// their correspond goals I need to find the least common multiple of these nrSteps.
let periodicities = [];
for ( let key in stepsToGoals ) {
  periodicities.push( stepsToGoals[key][0][1] );
}

nrSteps = findLeastCommonMultiple( periodicities );

console.log("\n\n--------------\nSecond part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log(stepsToGoals);

console.log('Number of steps ' + nrSteps);

