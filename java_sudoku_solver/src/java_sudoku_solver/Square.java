package java_sudoku_solver;

/**
 * @author George
 *
 */
public final class Square{
	
	int x;
	int y;
	boolean[] possibilities;
	
	public Square (int a, int b) {
		x = a;
		y = b;
		possibilities = new boolean[9];
        for (int i = 0; i <= 8; i++)
            possibilities[i] = true;	
	}
	
	public boolean certain () {
		int totalPos = 0;
        for (int i = 0; i <= 8; i++)
            if (possibilities[i] == true) {
            	totalPos = totalPos + 1;
            }
        if (totalPos == 1) {
            return true;
        }
        else {
        	return false;
        }
	}

}
