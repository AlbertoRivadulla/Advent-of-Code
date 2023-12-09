const fs = require('fs');


// Read the data
let data = fs.readFileSync('input.txt', 'utf-8').trim().split('\n');

// Read the different sequences
let sequences = [];
for ( let line of data ) {
  sequences.push( line.split(' ').map( (x) => Number(x) ) );
}

////////////////////////////////////////////////////////////////////////////////
// First part
////////////////////////////////////////////////////////////////////////////////

const checkSequenceZeroes = ( sequence ) => {
  for ( let el of sequence ) {
    if ( el != 0 ) {
      return false;
    }
  }
  return true;
}

const findNextNumber = ( sequence ) => {
  // If the sequence is made of zeroes, return zero.
  if ( checkSequenceZeroes( sequence ) ) {
    return 0;
  }

  // Compute the sequence below
  let sequenceBelow = Array( sequence.length - 1 );
  for ( let i = 0; i < sequence.length - 1; ++i ) {
    sequenceBelow[i] = sequence[i + 1] - sequence[i];
  }

  // Get the next value in the next sequence
  let nextValSequenceBelow = findNextNumber( sequenceBelow );
  
  // Compute the next value of the current sequence from that
  return sequence[ sequence.length - 1 ] + nextValSequenceBelow;
}

let startTime = Date.now();

// Find the next number in each sequence
let nextNumbers = Array( sequences.length );
let sumNextNumbers = 0;
for ( let i = 0; i < sequences.length; ++i ) {
  nextNumbers[i] = findNextNumber( sequences[i] );
  sumNextNumbers += nextNumbers[i];
}


console.log("\n\n--------------\nFirst part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Sum of the next numbers in the sequences: ' + sumNextNumbers);


////////////////////////////////////////////////////////////////////////////////
// Second part
////////////////////////////////////////////////////////////////////////////////

const findPreviousNumber = ( sequence ) => {
  // If the sequence is made of zeroes, return zero.
  if ( checkSequenceZeroes( sequence ) ) {
    return 0;
  }

  // Compute the sequence below
  let sequenceBelow = Array( sequence.length - 1 );
  for ( let i = 0; i < sequence.length - 1; ++i ) {
    sequenceBelow[i] = sequence[i + 1] - sequence[i];
  }

  // Get the previous value in the sequence below
  let previousValSequenceBelow = findPreviousNumber( sequenceBelow );
  
  // Compute the next value of the current sequence from that
  return sequence[0] - previousValSequenceBelow;
}

startTime = Date.now();

// Find the next number in each sequence
let previousNumbers = Array( sequences.length );
let sumPreviousNumbers = 0;
for ( let i = 0; i < sequences.length; ++i ) {
  previousNumbers[i] = findPreviousNumber( sequences[i] );
  sumPreviousNumbers += previousNumbers[i];
}

console.log("\n\n--------------\nSecond part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Sum of the previous numbers in the sequence: ' + sumPreviousNumbers);
