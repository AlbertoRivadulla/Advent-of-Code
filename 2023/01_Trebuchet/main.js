const fs = require('fs');

// Function to check if a character is a number
function isNumber( char ) {
  return ( char >= '0' && char <= '9' );
}

// Read the data
let data = fs.readFileSync('input.txt', 'utf-8').trim().split('\n');


////////////////////////////////////////////////////////////////////////////////
// First part
////////////////////////////////////////////////////////////////////////////////

let startTime = Date.now();

let sumCalibration = 0;
for ( const line of data ) {
  let thisNumber = '';
  // Iterate from the beginning until a number is found
  for ( let i = 0; i < line.length; ++i ) {
    if ( isNumber(line[i]) ) {
      thisNumber += line[i];
      break;
    }
  }
  // Iterate from the end until a number is found
  for ( let i = line.length - 1; i >= 0; --i ) {
    if ( isNumber(line[i]) ) {
      thisNumber += line[i];
      break;
    }
  }

  // Add this to the calibration sum
  sumCalibration += Number(thisNumber);
}

console.log("\n\n--------------\nFirst part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Calibration sum: ' + sumCalibration);


////////////////////////////////////////////////////////////////////////////////
// Second part
////////////////////////////////////////////////////////////////////////////////

startTime = Date.now();

// Numbers spelled
const spelledNrs = { 
  'one'   : '1', 
  'two'   : '2', 
  'three' : '3', 
  'four'  : '4', 
  'five'  : '5', 
  'six'   : '6', 
  'seven' : '7', 
  'eight' : '8', 
  'nine'  : '9'
};

sumCalibration = 0;
// for ( const line of data ) {
for ( let line of data ) {
  let thisNumber = '';

  // Find if there are numbers spelled, and create a dictionary with their positions
  // and values
  let leftSpelledInd = line.length;
  let rightSpelledInd = -1;
  let leftSpelledNr;
  let rightSpelledNr;
  for ( let number in spelledNrs ) {
    // If the number substring is found inside the string line, this will return
    // its index. Otherwise, it returns -1.
    let index = line.indexOf( number );
    while ( index != -1 ) {
      if ( index < leftSpelledInd ) {
        leftSpelledInd = index;
        leftSpelledNr = spelledNrs[number];
      }
      if ( index > rightSpelledInd ) {
        rightSpelledInd = index;
        rightSpelledNr = spelledNrs[number];
      }
      index = line.indexOf( number, index + 1 );
    }
  }

  // Iterate from the beginning until a number is found
  for ( let i = 0; i < line.length; ++i ) {
    if ( isNumber(line[i]) ) {
      // Check if this number is before the leftmost spelled one
      if ( i <= leftSpelledInd ) {
        thisNumber += line[i];
      } else {
        thisNumber += leftSpelledNr;
      }
      break;
    }
    // If no number was found, store the spelled ones
    if ( i === line.length - 1 ) {
      thisNumber = leftSpelledNr + rightSpelledNr;
    }
  }
  // Iterate from the end until a number is found
  for ( let i = line.length - 1; i >= 0; --i ) {
    if ( isNumber(line[i]) ) {
      // Check if this number is after the rightmost spelled one
      if ( i >= rightSpelledInd ) {
        thisNumber += line[i];
      } else {
        thisNumber += rightSpelledNr;
      }
      break;
    }
  }

  // Add this to the calibration sum
  sumCalibration += Number(thisNumber);
}


console.log("\n\n--------------\nSecond part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Calibration sum: ' + sumCalibration);
