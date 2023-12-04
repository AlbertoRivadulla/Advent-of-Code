const fs = require('fs');



// Read the data
let cards = fs.readFileSync('input.txt', 'utf-8').trim().split('\n');

////////////////////////////////////////////////////////////////////////////////
// First part
////////////////////////////////////////////////////////////////////////////////

let startTime = Date.now();

const computeMatches = ( card ) => {
  let cardSplit = card.match( /Card\s+(\d+):\s+((?:\d+\s+)+)\|\s+((?:\d+\s*)+)/ );

  // Split the winning numbers and my numbers
  let winningNrs = cardSplit[2].match( /\d+/g );
  let myNrs = cardSplit[3].match( /\d+/g );

  // Find how many numbers match
  let matches = 0;
  for ( const myNr of myNrs ) {
    for ( const winningNr of winningNrs ) {
      if ( myNr === winningNr )
        matches += 1;
    }
  }

  return matches;
}

let totalScore = 0;
for ( var card of cards) {
  let matches = computeMatches( card );

  // Compute the score
  if ( matches > 0 )
    totalScore += 2 ** ( matches - 1 );
}

console.log("\n\n--------------\nFirst part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Total score: ' + totalScore);


////////////////////////////////////////////////////////////////////////////////
// Second part
////////////////////////////////////////////////////////////////////////////////

startTime = Date.now();

let cardCopies = Array( cards.length ).fill( 1 );
for ( let i = 0; i < cards.length; ++i ) {
  let matches = computeMatches( cards[i] );

  // Add 1 copy of the next "matches" cards, for each copy of the current card
  for ( let j = i + 1; j <= i + matches && j < cards.length; ++j ) {
    cardCopies[j] += cardCopies[i];
  }
}

// Total amount of cards
let totalCardCopies = 0;
for ( const thisCardCopies of cardCopies )
  totalCardCopies += thisCardCopies;

console.log("\n\n--------------\nSecond part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Total amount of cards: ' + totalCardCopies);

