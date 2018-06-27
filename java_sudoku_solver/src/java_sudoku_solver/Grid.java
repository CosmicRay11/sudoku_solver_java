package java_sudoku_solver;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/*
 sudoku - an array of 9 strings of length 9, with the numbers 1-9 specifying
 what values are in the sudoku to be solved (0 represents blank space)

 gridList - a 9x9 array of Square objects that represent the squares on the board
 
 */


public final class Grid {
	
	String[] original;
	Square[][] gridList;
	
	public Grid(String[] sudoku) {
		original = sudoku;
		gridList = construct_gridList(sudoku);
		System.out.println(get_impactArray(0,0).length);
	}
	
	private Square[][] construct_gridList(String[] sudoku) {
		//create a 9x9 array of squares to represent the grid
		Square[][] gridList = new Square[9][9];
		for (int i=0;i<=8;i++) {
			for (int j=0; j<=8; j++) {
				//get the integer representation of the number at the required place in the sudoku
				String charNum = Character.toString(sudoku[i].charAt(j));
				int intNum = Integer.parseInt(charNum);
				
				//initialise the square at the current position
				gridList[i][j] = new Square(i,j);
				//if the square in the sudoku isn't blank, set its value to that in the sudoku
				if (intNum != 0) {
					gridList[i][j].set_value(intNum);
				}
			}
		}
		return gridList;
	}
	
	//gets the current total number of possibilities left for all squares
	private int get_progress() {
		int progress = 0;
		for (int i=0;i<=8;i++) {
			for (int j=0;j<=8;j++) {
				progress += gridList[i][j].count_possibilities();
			}
		}
		return progress;
	}
	
	private int[][] get_box(int x, int y) {
		
		 int[][] boxArray = new int[9][2];

		//java does integer division if the types of the operands are integer
		int boxX = x / 3;
		int boxY = y / 3;
		System.out.println(boxX);
		
		int count = 0;
		for (int i=boxX;i<=boxX+2;i++) {
			for (int j=boxY;j<=boxY+2;j++) {
				int[] intArray = {i,j};
				boxArray[count] = intArray;
				count ++;
			}
		}
		/*
		for (int i=0;i<=8;i++) {
			System.out.print(boxArray[i][0]);
			System.out.println(boxArray[i][1]);
		}
		*/
		return boxArray;
	}

	private int[][] get_row(int x) {
		int[][] rowArray = new int[9][2];
		for (int j=0;j<=8;j++) {
			int[] intArray = {x,j};
			rowArray[j] = intArray;
		}
		return rowArray;
	}

	private int[][] get_col(int y) {
		int[][] colArray = new int[9][2];
		for (int i=0;i<=8;i++) {
			int[] intArray = {i,y};
			colArray[i] = intArray;
		}
		return colArray;
	}
	
	private int[][] get_impactArray(int x, int y) {
		int[][] box = get_box(x,y);
		int[][] col = get_col(y);
		int[][] row = get_row(x);
		Set<int[]> impactSet = make_set(box);
		System.out.println(impactSet.size());
		Set<int[]> rowSet = make_set(row);
		Set<int[]> colSet = make_set(col);
		impactSet.addAll(rowSet);
		impactSet.addAll(colSet);
		int[] current = {x,y};
		System.out.println(impactSet.size());
		impactSet.remove(current);
		System.out.println(impactSet.size());
		System.out.println(impactSet.remove(current));
		int[][] impactArray = impactSet.toArray(new int[impactSet.size()][]);
		System.out.println(impactSet);
		print_nested(impactArray);
		return impactArray;
		
	}
	
	private Set<int[]> make_set (int[][] array) {
		Set<int[]> set = new HashSet<int[]>();
		for (int i=0;i<array.length;i++) {
			set.add(array[i]);
		}
		return set;
	}

	private void print_nested (int[][] array) {
		for (int i=0;i<array.length;i++) {
			for (int j=0; j<array[i].length;j++) {
				System.out.print(array[i][j]);
				if (j != array[i].length - 1) {
					System.out.print(",");
				}
			}
			System.out.println();
		}
	}
	
}
	
	/*
        def get_row(self, x):
        rowList = []
        for col in range(9):
            rowList.append(self.gridList[x][col])
        return rowList

}
*/
