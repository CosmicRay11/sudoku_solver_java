package java_sudoku_solver;

import java.util.ArrayList;
import java.util.List;

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
	
	private List<int[]> get_box(int x, int y) {
		
		List<int[]> boxList = new ArrayList<int[]>();

		//java does integer division if the types of the operands are integer
		int boxX = x / 3;
		int boxY = y / 3;
		
		for (int i=boxX;i<=boxX+2;i++) {
			for (int j=boxY;j<=boxY+2;j++) {
				int[] intArray = {i,j};
				boxList.add(intArray);
			}
		}
		return boxList;
	}
	
	private List<int[]> get_row(int x) {
		List<int[]> rowList = new ArrayList<int[]>();
		for (int j=0;j<=8;j++) {
			int[] intArray = {x,j};
			rowList.add(intArray);
		}
		return rowList;
	}

	private List<int[]> get_col(int y) {
		List<int[]> colList = new ArrayList<int[]>();
		for (int i=0;i<=8;i++) {
			int[] intArray = {i,y};
			colList.add(intArray);
		}
		return colList;
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
