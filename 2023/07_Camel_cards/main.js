const fs = require('fs');

// Value of the cards
let cardValues = {
  'A' : 12,
  'K' : 11,
  'Q' : 10,
  'J' : 9,
  'T' : 8,
  '9' : 7,
  '8' : 6,
  '7' : 5,
  '6' : 4,
  '5' : 3,
  '4' : 2,
  '3' : 1,
  '2' : 0
};

// The following returns 1 if hand1 is larger than hand2, and -1 otherwise
const compareTwoHands = ( hand1, hand2, value1, value2 ) => {
  if ( value1 > value2 )
    // return true;
    return 1;
  else if ( value1 < value2 )
    // return false;
    return -1;
  else {
    // If the two values are equal, compare the values of the single cards starting
    // at the beginning, until one has a larger value than the other.
    let i = 0;
    while ( i < hand1.length ) {
      if ( cardValues[hand1[i]] > cardValues[hand2[i]] ) 
        // return true;
        return 1;
      else if ( cardValues[hand1[i]] < cardValues[hand2[i]] ) 
        // return false;
        return -1;
      i++;
    }
  }
  // return false;
  return -1;
}


// Read the data
let data = fs.readFileSync('input.txt', 'utf-8').trim().split('\n');

// Parse the different hands
let hands = [];
for ( let line of data ) {
  line = line.split(' ');
  hands.push( [ line[0], Number(line[1]), 0 ] );
}

////////////////////////////////////////////////////////////////////////////////
// First part
////////////////////////////////////////////////////////////////////////////////

/*
  Values of the hands:
    Five of a kind  - 6
    Four of a kind  - 5
    Full house      - 4
    Three of a kind - 3
    Two pair        - 2
    One pair        - 1
    High card       - 0
*/
const getHandValue = ( hand ) => {
  // Count the cards of each type
  let cardsCount = {};
  for ( let card of hand ) {
    if ( card in cardsCount )
      cardsCount[card] += 1;
    else
      cardsCount[card] = 1;
  }
  // Get only the number of cards of each kind
  cardsCount = Object.values( cardsCount );

  switch ( cardsCount.length ) {
    case 1:
      // Five of a kind
      return 6;
    case 2:
      // Four of a kind or full house
      if ( cardsCount.includes(4) )
        return 5;
      else
        return 4;
    case 3:
      // Three of a kind or two pair
      if ( cardsCount.includes(3) )
        return 3;
      else
        return 2;
    case 4:
      // One pair
      return 1;
    case 5:
      // High card
      return 0;
  }
  return 0;
}


let startTime = Date.now();

// Compute the values of the different hands
for ( let i = 0; i < hands.length; ++i ) {
  hands[i][2] = getHandValue( hands[i][0] );
}

// Sort the hands based on their value
let handsSorted = hands.sort( ( x, y ) => { return compareTwoHands( x[0], y[0], x[2], y[2] ) } );

// Compute the total winnings from this
let totalWinnings = 0;
for ( let i = 0; i < handsSorted.length; ++i )
  totalWinnings += ( i + 1 ) * handsSorted[i][1];

console.log("\n\n--------------\nFirst part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Total winnings: ' + totalWinnings);


////////////////////////////////////////////////////////////////////////////////
// Second part
////////////////////////////////////////////////////////////////////////////////

// Types of cards to replace the Js with
const cardTypesNoJ = [ 'A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2' ];

// Get the combinations obtained by replacing recursively the different appearances
// of J
const getCombinations = ( hand, indicesOfJ ) => {
  if ( indicesOfJ.length === 0 )
    return [ hand ];

  // Replace the first occurence of J by each of the card types, and recursively
  // replace the rest
  let combinations = [];
  for ( let cardType of cardTypesNoJ ) {
    let thisHand = hand.substring(0, indicesOfJ[0]) + cardType + hand.substring(indicesOfJ[0]+1);
    // Recursively replace the rest of them
    combinations = combinations.concat( getCombinations( thisHand, indicesOfJ.slice(1) ) );
  }

  return combinations;
}

/*
  Values of the hands:
    Five of a kind  - 6
    Four of a kind  - 5
    Full house      - 4
    Three of a kind - 3
    Two pair        - 2
    One pair        - 1
    High card       - 0
*/
const getHandValueWithJokers = ( hand ) => {
  // Get the indices of the Js in the string
  let indicesOfJ = [];
  for ( let i = 0; i < hand.length; ++i ) {
    if ( hand[i] == 'J' )
      indicesOfJ.push( i );
  }

  // If the string does not contain a J, simply return its value
  if ( indicesOfJ.length === 0 )
    return getHandValue( hand );

  // Otherwise, compute the different combinations that are obtained by replacing the Js
  let combinations = getCombinations( hand, indicesOfJ );

  // Compute the maximum value obtained from the different combinations
  let maxValue = 0;
  for ( let comb of combinations ) {
    let thisValue = getHandValue( comb );
    if ( thisValue > maxValue ) {
      maxValue = thisValue;
    }
  }

  return maxValue;
}


startTime = Date.now();

// Modify the value of the card J
cardValues['J'] = -1;

// Compute the values of the different hands
for ( let i = 0; i < hands.length; ++i ) {
  hands[i][2] = getHandValueWithJokers( hands[i][0] );
}

// Sort the hands based on their value
let handsSortedWithJokers = hands.sort( ( x, y ) => { return compareTwoHands( x[0], y[0], x[2], y[2] ) } );

// Compute the total winnings from this
let totalWinningsWithJokers = 0;
for ( let i = 0; i < handsSortedWithJokers.length; ++i )
  totalWinningsWithJokers += ( i + 1 ) * handsSortedWithJokers[i][1];


console.log("\n\n--------------\nSecond part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Total winnings with jokers: ' + totalWinningsWithJokers);
