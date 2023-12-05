const fs = require('fs');

// Read the data
let almanac = fs.readFileSync('input.txt', 'utf-8').trim();

// Separate the seeds and the different maps in the almanac
almanac = almanac.split('\n\n');

// Seed numbers
let seeds = almanac[0].match(/\d+/g).map( (seed) => Number(seed) );

// Read the different maps
let maps = [];
for ( let i = 1; i < almanac.length; ++i ) {
  let thisAlmanacMap = almanac[i].split('\n');
  let thisMap = [];

  for ( const line of thisAlmanacMap.slice(1) ) {
    const theseNrs = line.match(/\d+/g).map( (nr) => Number(nr) );
    thisMap.push( {
      destStart   : theseNrs[0],
      sourceStart : theseNrs[1],
      length      : theseNrs[2]
    } );
  }

  maps.push(thisMap);
}


////////////////////////////////////////////////////////////////////////////////
// First part
////////////////////////////////////////////////////////////////////////////////

let startTime = Date.now();

const getDestinationNr = ( sourceNr, map ) => {
  for ( const range of map ) {
    // Check if the number is within the range
    let deltaSource = sourceNr - range.sourceStart;

    // If it is, return the corresponding destination value
    if ( deltaSource >= 0 && deltaSource < range.length ) {
      return range.destStart + deltaSource;
    }

  }
  // If the number is not in any of the ranges, return the same number
  return sourceNr;
}

// Propagate one seed number along the map
const propagateSeedNr = ( seedNr, maps ) => {
  let destination = seedNr;
  for ( const map of maps ) {
    destination = getDestinationNr( destination, map );
  }
  return destination;
}

// Propagate all the seeds in the map
let locations = seeds.map( (seed) => propagateSeedNr(seed, maps) );

// Get the smallest location number
let smallestLocation = 1000000000000;
// for ( const location of seedsPropagated ) {
for ( const location of locations ) {
  if ( location < smallestLocation )
    smallestLocation = location;
}

console.log("\n\n--------------\nFirst part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Smallest location: ' + smallestLocation);

////////////////////////////////////////////////////////////////////////////////
// Second part
////////////////////////////////////////////////////////////////////////////////

startTime = Date.now();

const propagateInterval = ( interval, map ) => {
  // Find where the map intervals cut the original interval
  // The elements of intervalCuts are:
  //  [ cut_start, cut_end, map_range_index ]
  let intervalCuts = [];
  for ( let i = 0; i < map.length; ++i ) {
    let leftCut  = Math.max( map[i].sourceStart, interval[0] );
    let rightCut = Math.min( map[i].sourceStart + map[i].length - 1, interval[1] );

    if ( leftCut < interval[1] && rightCut > interval[0] )
      intervalCuts.push( [ leftCut, rightCut, i ] );
  }

  // Sort the interval cuts according to their beginning
  intervalCuts = intervalCuts.sort( ( int1, int2 ) => { return int1[0] - int2[0] } );

  // Compute the resulting intervals
  let resultIntervals = [];
  let nr = interval[0];
  if ( intervalCuts.length > 0 ) {
    if ( nr < intervalCuts[0][0] ) {
      resultIntervals.push( [ nr, intervalCuts[0][0] - 1 ] );
      nr = intervalCuts[0][0];
    }
    for ( let i = 0; i < intervalCuts.length; ++i ) {
      let range = map[intervalCuts[i][2]];
      // Propagate this interval
      resultIntervals.push( [ range.destStart + ( intervalCuts[i][0] - range.sourceStart ),
                              range.destStart + ( intervalCuts[i][1] - range.sourceStart ) ]);

      nr = intervalCuts[i][1] + 1;
      // Propagate until the start of the next interval
      if ( i < intervalCuts.length - 1 ) {
        if ( nr < intervalCuts[i+1][0] )
          resultIntervals.push( [ nr, intervalCuts[i+1][0] - 1 ] );
      }
    }
  }
  // If there are numbers missing until the end, add these
  if ( nr < interval[1] )
    resultIntervals.push( [ nr, interval[1] ] );

  return resultIntervals;
}

// Convert the seeds to intervals
let seedIntervals = [];
let i = 0;
while ( i < seeds.length ) {
  seedIntervals.push( [ seeds[i], seeds[i] + seeds[i+1] - 1 ] );
  i += 2;
}

// Propagate the intervals in the map
let intervals = seedIntervals.map( ( interval ) => interval.slice() );
for ( const map of maps ) {

  let propagatedIntervals = [];

  for ( const thisInterval of intervals ) {
    let resultIntervals = propagateInterval( thisInterval, map );
    for ( const interval of resultIntervals )
      propagatedIntervals.push( interval );
  }

  intervals = propagatedIntervals;
}

// Get the minimum location
let smallestLocationPt2 = intervals.sort( ( int1, int2 ) => { return int1[0] - int2[0] } )[0][0];



console.log("\n\n--------------\nSecond part\n--------------");
console.log(`\t--- Execution time: ${(Date.now() - startTime)/1000} s ---\n\n`);

console.log('Smallest location ' + smallestLocationPt2);

