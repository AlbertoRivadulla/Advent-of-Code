const fs = require('fs');

const printSpringLine = ( springLine ) => {
  let string = '';
  for ( let spring of springLine ) {
    switch ( spring ) {
      case 0:
        string += '.';
        break;
      case 1:
        string += '#';
        break;
      case 2:
        string += '?';
        break;
    }
  }
  console.log( string );
}

// Read the data
let data = fs.readFileSync('input.txt', 'utf-8').trim().split('\n');

// Parse the data
/*
  States of the springs:
    0 -> working (.)
    1 -> damaged (#)
    2 -> unknown (?)
*/
let springs = [];
for ( let line of data ) {
  line = line.split(' ');

  // Read the state of the springs
  let states = [];
  for ( let i = 0; i < line[0].length; ++i ) {
    if ( line[0][i] === '.' ) {
      states.push(0);
    }
    if ( line[0][i] === '#' ) {
      states.push(1);
    }
    if ( line[0][i] === '?' ) {
      states.push(2);
    }
  }

  // Read the numbers
  let numbers = line[1].split(',').map((x) => Number(x));

  springs.push( [ states, numbers ] );
}


////////////////////////////////////////////////////////////////////////////////
// First part
////////////////////////////////////////////////////////////////////////////////

// // Check if a combination is valid
// const isCombinationValid = ( comb, numbers ) => {
//   let nrDamagedTarget = 0;
//   console.log('numbers ' + numbers);
//   for ( let nr of numbers ) {
//     nrDamagedTarget += nr;
//   }
//
//   let nrDamagedReal = 0;
//   for ( let spring of comb ) {
//     if ( spring === 1 ) {
//       nrDamagedReal += 1;
//     }
//   }
//
//   return nrDamagedTarget === nrDamagedReal;
// }

// Get the different combinations admitted by a line of springs and a series of numbers
const getCombinations = ( springs, numbers ) => {

  // Check if the result is in the cache

  if ( numbers.length === 0 ) {
    // If there are still unknown springs at the end, mark them as working
    let combination = springs.slice();
    for ( let i = 0; i < combination.length; ++i ) {
      if ( combination[i] === 2 ) {
        combination[i] = 0;
      }
    }

    // If there is any spring not working here, this is not valid
    for ( let spring of springs ) {
      if ( spring === 1 ) {
        return [];
      }
    }

    return [ combination ];
  }

  let combinations = [];

  // Find the combinations taking into account the first number
  let combsFirstNr = [];
  // Find the different spots where I can place numbers[1] damaged springs
  for ( let i = 0; i < springs.length; ++i ) {
    let available = true;
    // Check that the springs before are unknown or not working.
    for ( let j = 0; j < i; ++j ) {
      if ( springs[j] === 1 ) {
        available = false;
        break;
      }
    }

    // Check that the numbers[0] springs are damaged or unknown.
    for ( let j = 0; j < numbers[0]; ++j ) {
      if ( springs[i + j] === 0 ) {
        available = false;
        break;
      }
    }

    if ( !available ) {
      continue;
    }

    if ( springs.length < i + numbers[0] ) {
      continue;
    }

    if ( !(springs[i + numbers[0]] === 1) ) {
      // In this case it is available, so I construct this combination
      let thisFirstComb = springs.slice( 0, i + numbers[0] + 1 );
      // Mark working springs before
      if ( i > 0 ) {
        for ( let j = 0; j < i; ++j ) {
          thisFirstComb[ j ] = 0;
        }
      }
      // Mark damaged springs
      for ( let j = i; j < i + numbers[0]; ++j ) {
        thisFirstComb[ j ] = 1;
      }
      if ( thisFirstComb.length > i + numbers[0] ) {
        // One working spring at the end
        thisFirstComb[ i + numbers[0] ] = 0;
      }

      combsFirstNr.push( thisFirstComb );
    }
  }

  if ( combsFirstNr.length === 0 ) {
    return [];
  }

  // For each of the combinations found before, find the available combinations
  // for the rest of the spring.
  for ( let firstComb of combsFirstNr ) {
    let nextCombs = getCombinations( springs.slice( firstComb.length ), numbers.slice(1) );
    if ( nextCombs.length > 0 ) {
      for ( let nextComb of nextCombs ) {
        combinations.push( firstComb.concat( nextComb ) );
      }
    }
  }

  return combinations;
}


let startTime = Date.now();

// Find the amount of combinations possible for each line
let nrCombinations = [];
for ( let springsLine of springs ) {
  // console.log( '\n\n====================================' );
  // printSpringLine( springsLine[0] );
  // console.log( springsLine[1] );
  // console.log('----------------------');

  // Get the different combinations available for this line of springs
  let combinations = getCombinations( springsLine[0], springsLine[1] );
  nrCombinations.push( combinations.length );
  // console.log('Number of combinations: ' + combinations.length);
}

// Total number of combinations
let nrCombinationsTotal = 0;
for ( let nr of nrCombinations ) {
  nrCombinationsTotal += nr;
}


console.log("\n\n--------------\nFirst part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log("Total number of combinations: " + nrCombinationsTotal);


////////////////////////////////////////////////////////////////////////////////
// Second part
////////////////////////////////////////////////////////////////////////////////

const unfoldSpringLine = ( springLine, nrUnfolds = 5 ) => {
  // Repeat the sequence of springs 5 times, with a ? between copies
  // Repeat the sequence of numbers 5 times, with a 0 at the beginning
  let springsUnfolded = [];
  let numbersUnfolded = [ 0 ];
  for ( let i = 0; i < nrUnfolds; ++i ) {
    springsUnfolded = springsUnfolded.concat( springLine[0] ).concat( [ 2 ] );
    numbersUnfolded = numbersUnfolded.concat( springLine[1] );
  }

  return [ springsUnfolded, numbersUnfolded ];
}

const countCombinations = ( springs, numbers ) => {

  // Counts for each spring index and number index
  let counts = [];
  for ( let i = 0; i < springs.length; ++i ) {
    counts[ i ] = [];
  }

  // Function that return the amount of counts up to this point
  let getCounts = ( sprInd, nrInd ) => {
    // If I am at the beginning of the sequence of springs and numbers, return 1
    if ( sprInd === -1 && nrInd === 0 ) {
      return 1;
    }
    if ( counts[sprInd] ) {
      // This returns counts[sprInd][nrInd] if this quantity exists, and otherwise
      // returns zero.
      return counts[sprInd][nrInd] ?? 0;
    }
    return 0;
  }

  // Iterate over the numbers
  for ( let nrInd = 0; nrInd < numbers.length; ++nrInd ) {
    // Iterate over the springs
    for ( let sprInd = 0; sprInd < springs.length; ++sprInd ) {
      let currentCount = 0;

      // If the current spring is not damaged
      if ( springs[sprInd] != 1 ) {
        currentCount += getCounts( sprInd - 1, nrInd );
      }

      // If I am after the 1st number
      // if ( nrInd > 0 ) {
      if ( true ) {
        let doCount = true;
        for ( let k = 1; k <= numbers[nrInd]; ++k ) {
          // If in the next numbers[nrInd] springs there is an undamaged one, there
          // is nothing to count.
          if ( springs[sprInd - k] === 0 ) {
            doCount = false;
            // break;
          }
        }
        if ( springs[sprInd] === 1 ) {
          doCount = false;
        }
        if ( doCount ) {
          currentCount += getCounts( sprInd - numbers[nrInd] - 1, nrInd - 1 );
        }
      }

      counts[sprInd][nrInd] = currentCount;
    }
  }

  return counts[springs.length - 1][numbers.length - 1];
}

startTime = Date.now();

// Unfold the lines of springs
let springsUnfolded = [];
for ( let springLine of springs ) {
  springsUnfolded.push( unfoldSpringLine( springLine ) );
}


// Find the amount of combinations possible for each line, and sum them
// nrCombinations = [];
let i = 0;
nrCombinationsTotal = 0;
for ( let springsLine of springsUnfolded ) {
  // console.log( '\n\n====================================' );
  // printSpringLine( springsLine[0] );
  // console.log('----------------------');

  let thisNrCombinations = countCombinations( springsLine[0], springsLine[1] );
  nrCombinationsTotal += thisNrCombinations;

  // console.log('Number of combinations: ' + thisNrCombinations);
}

console.log("\n\n--------------\nSecond part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);


console.log("Total number of combinations: " + nrCombinationsTotal);
