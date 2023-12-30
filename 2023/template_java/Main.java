import java.time.Instant;
import java.time.Duration;

import java.io.File;
import java.util.Scanner;

public class Main {
  public static void main( String[] args ) throws Exception {

    // Read the data
    File inputFile = new File( "input.txt" );
    Scanner scanner = new Scanner( inputFile );

    while ( scanner.hasNextLine() ) {
      String thisLine = scanner.nextLine();

      //
      //
    }



    ////////////////////////////////////////////////////////////////////////////////
    // First part
    ////////////////////////////////////////////////////////////////////////////////

    long startTime = System.currentTimeMillis();


    System.out.println("\n\n--------------\nFirst part\n--------------");
    System.out.println("\t--- Execution time: " + (System.currentTimeMillis() - startTime) + " ms ---\n\n");


    ////////////////////////////////////////////////////////////////////////////////
    // Second part
    ////////////////////////////////////////////////////////////////////////////////

    startTime = System.currentTimeMillis();




    System.out.println("\n\n--------------\nSecond part\n--------------");
    System.out.println("\t--- Execution time: " + (System.currentTimeMillis() - startTime) + " ms ---\n\n");
  }
}

