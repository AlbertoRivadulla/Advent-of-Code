import java.time.Instant;
import java.time.Duration;

import java.io.File;
import java.util.Scanner;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.HashMap;
import java.util.regex.Pattern;
import java.util.regex.Matcher;


record Instruction( int boxNr, String lensLabel, int focalLength ) {}

record Lens( String lensLabel, int focalLength ) {
  @Override
  public String toString() {
    return "[ " + lensLabel + " " + focalLength + " ]";
  }

}

public class Main {

  public static int computeHash( String string ) {
    int currValue = 0;

    // Compute the hash value as given in the instructions
    for ( int i = 0; i < string.length(); ++i ) {
      // Increment the hash by the ASCII value of the current character
      currValue += (int)string.charAt(i);
      // Multiply the hash by 17
      currValue *= 17;
      // Compute the remainder of dividing by 256
      currValue %= 256;
    }

    return currValue;
  }


  public static void main( String[] args ) throws Exception {

    // Read the data
    ArrayList<String> initSteps = new ArrayList<>();

    File inputFile = new File( "input.txt" );
    Scanner scanner = new Scanner( inputFile );

    while ( scanner.hasNextLine() ) {
      String thisLine = scanner.nextLine();

      Pattern p = Pattern.compile( "((\\w+)=?([0-9]*-*)),?" );
      Matcher m = p.matcher( thisLine );

      // Find the elements in the different capture groups
      while ( m.find() ) { 
        // // Level 0: entire reg expression
        // System.out.println( m.group() ); 
        // // Level 1: global parenthesis (leaves out the comma)
        // System.out.println( m.group(1) ); 
        // // Level 2: first parenthesis
        // System.out.println( m.group(2) ); 
        // // Level 3: second parenthesis
        // System.out.println( m.group(3) ); 

        // Store this in the list of initial steps
        initSteps.add( m.group(1) );
      } 

    }


    ////////////////////////////////////////////////////////////////////////////////
    // First part
    ////////////////////////////////////////////////////////////////////////////////

    long startTime = System.currentTimeMillis();

    // Compute the sum of the hash values of the instructions
    int sumHashValues = 0;
    for ( String instruction : initSteps ) {
      int hashValue = computeHash( instruction );
      sumHashValues += hashValue;
    }


    System.out.println("\n\n--------------\nFirst part\n--------------");
    System.out.println("\t--- Execution time: " + (System.currentTimeMillis() - startTime) + " ms ---\n\n");
    System.out.println("Sum of hash values: " + sumHashValues);


    ////////////////////////////////////////////////////////////////////////////////
    // Second part
    ////////////////////////////////////////////////////////////////////////////////

    startTime = System.currentTimeMillis();

    // Read the instructions
    ArrayList<Instruction> instructions = new ArrayList<>();
    for ( String instruction : initSteps ) {
      // Separate the instruction in two parts
      Pattern p = Pattern.compile( "(\\w+)(.+)" );
      Matcher m = p.matcher( instruction );

      while ( m.find() ) {
        String lensLabel = m.group(1);

        // The hash of the first group of the match is the lens label
        int boxNr = computeHash( lensLabel );

        // Get the instruction from the second group of the match
        int focalLength;
        if ( m.group(2).charAt(0) == '-' ) {
          focalLength = -1;
        }
        else {
          focalLength = Integer.parseInt( m.group(2).substring(1) );
        }

        // instructions.add( new int[] { lensLabel, focalLength } );
        instructions.add( new Instruction( boxNr, lensLabel, focalLength ) );
      }
    }

    // Initialize the list of boxes
    ArrayList<LinkedList<Lens>> boxes = new ArrayList<>(256);
    for ( int i = 0; i < 256; ++i ) {
      boxes.add( new LinkedList<Lens>() );
    }

    // Perform the operations
    for ( Instruction instr : instructions ) {
      // If the instruction starts with a '-', which I encoded with a negative focal length
      if ( instr.focalLength() < 0 ) {
        // Go to the box, and remove the lens with the given label if it exists
        for ( int i = 0; i < boxes.get(instr.boxNr()).size(); ++i ) {
          // System.out.println( boxes.get(instr.boxNr()).get(i).lensLabel() + " " + instr.lensLabel());
          if( boxes.get(instr.boxNr()).get(i).lensLabel().equals(instr.lensLabel()) ) {
          // if ( boxes.get(instr.boxNr()).get(i).lensLabel() == instr.lensLabel() ) {
            // System.out.println("removing");
            boxes.get(instr.boxNr()).remove(i);
            break;
          }
        }
      }
      // Otherwise, the instruction starts with a '='
      else {
        // If there is a lens in the box with the same label, replace it by the new one
        boolean lensAlreadyPresent = false;
        for ( int i = 0; i < boxes.get(instr.boxNr()).size(); ++i ) {
          if ( boxes.get(instr.boxNr()).get(i).lensLabel().equals(instr.lensLabel()) ) {
            // Remove the old one
            boxes.get(instr.boxNr()).remove(i);
            // Add the new one
            boxes.get(instr.boxNr()).add( i, new Lens( instr.lensLabel(), instr.focalLength() ) );
            lensAlreadyPresent = true;
          }
        }

        // Otherwise, simply add the new one
        if ( !lensAlreadyPresent ) {
          boxes.get(instr.boxNr()).add( new Lens( instr.lensLabel(), instr.focalLength() ) );
        }
      }
    }

    // Compute the total focusing power
    int totalPower = 0;
    for ( int i = 0; i < boxes.size(); ++i ) {
      for ( int j = 0; j < boxes.get(i).size(); ++j ) {
        totalPower += (i+1) * (j+1) * boxes.get(i).get(j).focalLength();
      }
    }

    System.out.println("\n\n--------------\nSecond part\n--------------");
    System.out.println("\t--- Execution time: " + (System.currentTimeMillis() - startTime) + " ms ---\n\n");
    System.out.println("Total focusing power: " + totalPower);
  }
}

