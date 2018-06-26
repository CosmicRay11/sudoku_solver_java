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
	
	public void set_value(int value) {
		if (value <= 9 && value >=1) {
			for (int i=0;i<=8;i++) {
				if (i != value-1) {
					possibilities[i] = false;
				}
				else {
					possibilities[i] = true;
				}
			}
		}
	}
	
	public int count_possibilities () {
		int totalPos = 0;
        for (int i = 0; i <= 8; i++)
            if (possibilities[i] == true) {
            	totalPos = totalPos + 1;
            }
        return totalPos;
	}
	
	public void remove_possibility (int num) {
		// num is the number that has been eliminated as a possibility from the square
		if (num >= 1 && num <= 9) {
			int index = num - 1;
			possibilities[index] = false;
		}
	}
	
	public int get_value ()  {
		if (certain()) {
			for (int i = 0; i <= 8; i++) {
				if (possibilities[i] == true) {
					return i+1;
				}
			}
		}
		//only used to stop eclipse throwing its toys out the pram complaining there's no return int statement
	    return 0;
	}
	
	public boolean certain () {
		int count = count_possibilities();
		if (count == 1) {
			return true;
		}
		else {
			return false;
		}
	}

	public boolean impos () {
		int count = count_possibilities();
		if (count == 0) {
			return true;
		}
		else {
			return false;
		}
	}
}
