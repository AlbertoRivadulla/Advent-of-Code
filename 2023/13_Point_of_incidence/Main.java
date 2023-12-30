import java.time.Instant;
import java.time.Duration;

import java.io.File;
import java.util.Scanner;

import java.util.ArrayList;

public class Main {

  /*
  * Find the column or row of symmetry of a map.
  * It returns to values:
  *   - Index of the column/row of symmetry.
  *   - Flag saying whether it is a column (0) or a row (1).
  */
  public static int[] findPointOfSymmetry( ArrayList<ArrayList<Integer>> map, int[] oldSymmetry ) {
    // Check symmetry with respect to each column
    for ( int j = 1; j < map.get(0).size(); j++ ) {
      boolean isSymmetry = true;
      for ( int delta = 0; j-1-delta >= 0 && j+delta < map.get(0).size(); delta++ ) {
        for ( int i = 0; i < map.size(); ++i ) { 
          if ( map.get(i).get(j-1-delta) != map.get(i).get(j+delta) ) {
            isSymmetry = false;
            break;
          }
        }
        if ( !isSymmetry ) {
          break;
        }
      }

      if ( isSymmetry && !( oldSymmetry[0] == j && oldSymmetry[1] == 0 ) ) {
        return new int[] { j, 0 };
      }
    }

    // Check symmetry with respect to each row
    for ( int i = 1; i < map.size(); i++ ) {
      boolean isSymmetry = true;
      for ( int delta = 0; i-1-delta >= 0 && i+delta < map.size(); delta++ ) {
        for ( int j = 0; j < map.get(0).size(); ++j ) { 
          if ( map.get(i-1-delta).get(j) != map.get(i+delta).get(j) ) {
            isSymmetry = false;
            break;
          }
        }
        if ( !isSymmetry ) {
          break;
        }
      }

      if ( isSymmetry && !( oldSymmetry[0] == i && oldSymmetry[1] == 1 ) ) {
        return new int[] { i, 1 };
      }
    }

    return new int[] { 0, -1 };
  }

  /*
  * Find the column or row of symmetry of a map, assuming it has exactly one smudge.
  * This means that one value is not correct.
  * It returns to values:
  *   - Index of the column/row of symmetry.
  *   - Flag saying whether it is a column (0) or a row (1).
  */
  public static int[] findPointOfSymmetryWithSmudge( ArrayList<ArrayList<Integer>> map ) {
    // Compute the original reflection
    int[] originalSymmetry = findPointOfSymmetry( map, new int[] { 0, -1 } );

    // Iterate over the different positions where the smudge can be
    for ( int i = 0; i < map.size(); ++i ) {
      for ( int j = 0; j < map.get(0).size(); ++j ) {
        map.get(i).set( j, (map.get(i).get(j) + 1) % 2 );
        int[] symmetry = findPointOfSymmetry( map, originalSymmetry );
        // Put the map back in its original form
        map.get(i).set( j, (map.get(i).get(j) + 1) % 2 );
        if ( symmetry[1] != -1 ) {
          return symmetry;
        }
      }
    }
    return new int[] { 0, -1 };
  }

  public static void main( String[] args ) throws Exception {

    // Read the maps
    ArrayList<ArrayList<ArrayList<Integer>>> maps = new ArrayList<>();

    File inputFile = new File( "input.txt" );
    Scanner scanner = new Scanner( inputFile );

    int mapIndex = 0;
    int thisMapLine = 0;

    maps.add( new ArrayList<>() );

    while ( scanner.hasNextLine() ) {
      String thisLine = scanner.nextLine();

      if ( thisLine == "" ) {
        mapIndex += 1;
        thisMapLine = 0;
        maps.add( new ArrayList<>() );
        continue;
      }

      // Initialize the line of the map
      maps.get(mapIndex).add( new ArrayList<Integer>() );

      for ( int i = 0; i < thisLine.length(); ++i ) {
        if ( thisLine.charAt(i) == '.' ) {
          maps.get(mapIndex).get(thisMapLine).add( 0 );
        }
        else {
          maps.get(mapIndex).get(thisMapLine).add( 1 );
        }
      }

      thisMapLine += 1;
    }


    ////////////////////////////////////////////////////////////////////////////////
    // First part
    ////////////////////////////////////////////////////////////////////////////////

    long startTime = System.currentTimeMillis();

    // Find the column or row of symmetry for each map, and from this compute the
    // number that summarizes the reflections.
    int summarizingNr = 0;
    for ( int i = 0; i < maps.size(); ++i ) {
      int[] thisSymmetry = findPointOfSymmetry( maps.get(i), new int[] { 0, -1 } );
      // For symmetry with respect to a column, add the column number 
      if ( thisSymmetry[1] == 0 ) {
        summarizingNr += thisSymmetry[0];
      }
      // For symmetry with respect to a row, add the row number multiplied by 100
      if ( thisSymmetry[1] == 1 ) {
        summarizingNr += 100 * thisSymmetry[0];
      }
      // System.out.println( thisSymmetry[0] + "     " + thisSymmetry[1] );
    }

    System.out.println("\n\n--------------\nFirst part\n--------------");
    System.out.println("\t--- Execution time: " + (System.currentTimeMillis() - startTime) + " ms ---\n\n");
    System.out.println("Symmarizing number: " + summarizingNr);


    ////////////////////////////////////////////////////////////////////////////////
    // Second part
    ////////////////////////////////////////////////////////////////////////////////

    startTime = System.currentTimeMillis();

    // Find the column or row of symmetry for each map after fixing a smudge.
    // Again, compute the number that summarizes the reflections.
    summarizingNr = 0;
    for ( int i = 0; i < maps.size(); ++i ) {
      int[] thisSymmetry = findPointOfSymmetryWithSmudge( maps.get(i) );
      // For symmetry with respect to a column, add the column number 
      if ( thisSymmetry[1] == 0 ) {
        summarizingNr += thisSymmetry[0];
      }
      // For symmetry with respect to a row, add the row number multiplied by 100
      if ( thisSymmetry[1] == 1 ) {
        summarizingNr += 100 * thisSymmetry[0];
      }
      // System.out.println( thisSymmetry[0] + "     " + thisSymmetry[1] );
    }


    System.out.println("\n\n--------------\nSecond part\n--------------");
    System.out.println("\t--- Execution time: " + (System.currentTimeMillis() - startTime) + " ms ---\n\n");
    System.out.println("Symmarizing number: " + summarizingNr);
  }
}

