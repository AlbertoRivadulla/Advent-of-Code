import java.time.Instant;
import java.time.Duration;

import java.io.File;
import java.util.Scanner;
import java.util.ArrayList;

public class Main {

  static void tiltMapNorth( ArrayList<ArrayList<Integer>> map ) {
    // Iterate over the rows, starting at the top
    for ( int i = 0; i < map.size(); ++i ) {
      for ( int j = 0; j < map.get(0).size(); ++j ) {
        // If there is a round rock at this location, move it up
        if ( map.get(i).get(j) == 1 ) {
          // Go up from this point until I can go no further
          int iFinal = i;
          while ( iFinal > 0 && map.get(iFinal - 1).get(j) == 0 ) {
            iFinal -= 1;
          }
          map.get(i).set( j, 0 );
          map.get(iFinal).set( j, 1 );
        }
      }
    }
  }

  static void tiltMapCycle( ArrayList<ArrayList<Integer>> map ) {
    // Tilt the map north
    for ( int i = 0; i < map.size(); ++i ) {
      for ( int j = 0; j < map.get(0).size(); ++j ) {
        // If there is a round rock at this location, move it up
        if ( map.get(i).get(j) == 1 ) {
          // Go up from this point until I can go no further
          int iFinal = i;
          while ( iFinal > 0 && map.get(iFinal - 1).get(j) == 0 ) {
            iFinal -= 1;
          }
          map.get(i).set( j, 0 );
          map.get(iFinal).set( j, 1 );
        }
      }
    }

    // Tilt the map west
    for ( int j = 0; j < map.get(0).size(); ++j ) {
      for ( int i = 0; i < map.size(); ++i ) {
        if ( map.get(i).get(j) == 1 ) {
          int jFinal = j;
          while ( jFinal > 0 && map.get(i).get(jFinal - 1) == 0 ) {
            jFinal -= 1;
          }
          map.get(i).set( j, 0 );
          map.get(i).set( jFinal, 1 );
        }
      }
    }

    // Tilt the map south
    for ( int i = map.size()-1; i >= 0; --i ) {
      for ( int j = 0; j < map.get(0).size(); ++j ) {
        if ( map.get(i).get(j) == 1 ) {
          int iFinal = i;
          while ( iFinal < map.size()-1 && map.get(iFinal + 1).get(j) == 0 ) {
            iFinal += 1;
          }
          map.get(i).set( j, 0 );
          map.get(iFinal).set( j, 1 );
        }
      }
    }


    // Tilt the map east
    for ( int j = map.get(0).size()-1; j >= 0; --j ) {
      for ( int i = 0; i < map.size(); ++i ) {
        if ( map.get(i).get(j) == 1 ) {
          int jFinal = j;
          while ( jFinal < map.get(0).size()-1 && map.get(i).get(jFinal + 1) == 0 ) {
            jFinal += 1;
          }
          map.get(i).set( j, 0 );
          map.get(i).set( jFinal, 1 );
        }
      }
    }

  }

  static int computeTotalLoad( ArrayList<ArrayList<Integer>> map ) {
    int load = 0;
    for ( int i = 0; i < map.size(); ++i ) {
      int loadCurrentRow = map.size() - i;
      for ( int j = 0; j < map.get(0).size(); ++j ) {
        if ( map.get(i).get(j) == 1 ) {
          load += loadCurrentRow;
        }
      }
    }

    return load;
  }

  public static void main( String[] args ) throws Exception {

    // Read the map
    /*
      . (floor)       -> 0
      O (round rock)  -> 1
      # (square rock) -> 2
    */
    ArrayList<ArrayList<Integer>> originalMap = new ArrayList<>();
    File inputFile = new File( "input.txt" );
    Scanner scanner = new Scanner( inputFile );

    while ( scanner.hasNextLine() ) {
      String thisLine = scanner.nextLine();

      ArrayList<Integer> thisMapLine = new ArrayList<>();
      for ( int i = 0; i < thisLine.length(); ++i ) {
        switch ( thisLine.charAt(i) ) {
          case 'O':
            thisMapLine.add( 1 );
            break;
          case '#':
            thisMapLine.add( 2 );
            break;
          default:
            thisMapLine.add( 0 );
        }
      }

      originalMap.add( thisMapLine );
    }


    ////////////////////////////////////////////////////////////////////////////////
    // First part
    ////////////////////////////////////////////////////////////////////////////////

    long startTime = System.currentTimeMillis();

    // Copy the map
    ArrayList<ArrayList<Integer>> map = new ArrayList<>();
    for ( ArrayList<Integer> line : originalMap ) {
      ArrayList<Integer> lineCopy = new ArrayList<>(line);
      map.add( lineCopy );
    }

    // Tilt the map north and compute the total load
    tiltMapNorth( map );
    int totalLoad = computeTotalLoad( map );

    System.out.println("\n\n--------------\nFirst part\n--------------");
    System.out.println("\t--- Execution time: " + (System.currentTimeMillis() - startTime) + " ms ---\n\n");
    System.out.println("Total load: " + totalLoad);


    ////////////////////////////////////////////////////////////////////////////////
    // Second part
    ////////////////////////////////////////////////////////////////////////////////

    startTime = System.currentTimeMillis();

    // Copy the map
    map = new ArrayList<>();
    for ( ArrayList<Integer> line : originalMap ) {
      ArrayList<Integer> lineCopy = new ArrayList<>(line);
      map.add( lineCopy );
    }

    // Number of cycles
    int nCycles = 1000000000;
    // List of total loads
    ArrayList<Integer> totalLoads = new ArrayList<>();

    // Variables to find the periodicity of the process
    boolean possiblePeriodicity = false;
    int startPeriodicity = 0;
    int endPeriodicity = 0;

    // Offset and period that I need to find
    int offset = 0;
    int period = 0;

    for ( int i = 0; i < nCycles; ++i ) {
      // Tilt the map and compute the toal load
      tiltMapCycle( map );
      int thisTotalLoad = computeTotalLoad( map );
      totalLoads.add( thisTotalLoad );

      // Check that the periodicity is not broken
      if ( possiblePeriodicity ) {
        if ( !( totalLoads.get(startPeriodicity + i - endPeriodicity) == thisTotalLoad ) ){
          possiblePeriodicity = false;
        }
        if ( (i - endPeriodicity) == (endPeriodicity - startPeriodicity) ) {
          offset = startPeriodicity;
          period = endPeriodicity - startPeriodicity;
          if ( period > 1 ) {
            break;
          }
        }
      }
      // If not possible periodicity, check if there is a load before with the 
      // same value as the current one
      else {
        for ( int j = 0; j < i; ++j ) {
          if ( totalLoads.get(j) == thisTotalLoad ) {
            possiblePeriodicity = true;
            startPeriodicity = j;
            endPeriodicity = i;
          }
        }
      }
    }

    // Copy again the original map
    map = new ArrayList<>();
    for ( ArrayList<Integer> line : originalMap ) {
      ArrayList<Integer> lineCopy = new ArrayList<>(line);
      map.add( lineCopy );
    }

    // Perform the offset and remaining tilt cycles in the map
    int remainingCycles = ( nCycles - offset ) % period;
    for ( int i = 0; i < remainingCycles + offset; ++i ) {
      tiltMapCycle( map );
    }
    // Compute the load at the end
    totalLoad = computeTotalLoad( map );

    System.out.println("\n\n--------------\nSecond part\n--------------");
    System.out.println("\t--- Execution time: " + (System.currentTimeMillis() - startTime) + " ms ---\n\n");
    System.out.println("Total load: " + totalLoad);
  }
}

