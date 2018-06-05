'''
Created on 15 Apr 2018

@author: George
'''
#Sudoku solving problem OOP
from idlelib.idle_test.test_replace import orig_mbox

class Square(object):
    
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.possibilities = [1,2,3,4,5,6,7,8,9]
    
    def certain(self):
        if len(self.possibilities) == 1:
            return True
        return False
    
    def impos(self):
        if len(self.possibilities) < 1:
            return True
        return False

    def remove_pos(self, pos):
        try:
            self.possibilities.remove(pos)
        except ValueError:
            pass
    
    def value(self):
        return self.possibilities[0]

class Grid(object):
    
    def __init__(self, sudoku):
        self.original = sudoku
        self.gridList = []
        
        for row in range(9):
            self.gridList.append([])
            for col in range(9):
                self.gridList[row].append(Square(row, col))
                
                num = int(sudoku[row][col])
                if num != 0:
                    self.gridList[row][col].possibilities = [num]
 
    def get_progress(self):
        progress = 0
        for x in range(9):
            for y in range(9):
                progress += len(self.gridList[x][y].possibilities)
        return progress

    def get_box(self, x, y):
        boxX = x//3 * 3
        boxY = y//3 * 3
        boxList = []
        for row in range(boxX, boxX + 3):
            for col in range(boxY, boxY + 3):
                boxList.append(self.gridList[row][col])
        return boxList

    def get_row(self, x):
        rowList = []
        for col in range(9):
            rowList.append(self.gridList[x][col])
        return rowList

    def get_col(self, y):
        colList = []
        for row in range(9):
            colList.append(self.gridList[row][y])
        return colList

    def get_impactSet(self, x, y):
        box = self.get_box(x,y)
        row = self.get_row(x)
        col = self.get_col(y)
        impactSet = set(box+row+col)
        impactSet.remove(self.gridList[x][y])
        return impactSet

    def is_solved(self):
        #check there is only one number per square
        for x in range(9):
            for y in range(9):
                if len(self.gridList[x][y].possibilities) != 1:
                    return False

        #check all rows work
        for x in range(9):
            rowList = []
            for y in range(9):
                rowList.append(self.gridList[x][y].possibilities[0])
            if sorted(rowList) != list(range(1,10)):
                return False

        #check all columns work
        for y in range(9):
            colList = []
            for x in range(9):
                colList.append(self.gridList[x][y].possibilities[0])
            if sorted(colList) != list(range(1,10)):
                return False

        boxCoordList = [((x//3)*3, (x%3)*3) for x in range(9)]
        for box in boxCoordList:
            boxX = box[0]
            boxY = box[1]
            boxList = []
            for x in range(boxX, boxX + 3):
                for y in range(boxY, boxY + 3):
                    boxList.append(self.gridList[x][y].possibilities[0])
            if sorted(boxList) != list(range(1,10)):
                return False
        
        return True
        
    def works(self):
        for x in range(9):
            for y in range(9):
                if len(self.gridList[x][y].possibilities) not in range(1,10):
                    return False
        return True
  
    def solve(self):
        working = True
        method = 0
        while working and not self.is_solved() and self.works():
            statusBefore = self.get_progress()
            
            if method == 0:
                for x in range(9):
                    for y in range(9):
                        self.reduce_possibilities(x,y)
            
            elif method == 1:
                #generate x,y coordinates that cover all columns, rows and boxes
                for x in range(9):
                    y = x*3 - (8* (x//3))
                    self.assign_place(x,y)
                     
            elif method == 2:
                #generate x,y coordinates that cover all boxes
                for x in range(9):
                    y = x*3 - (8* (x//3))
                    self.claim_row(x, y)
                     
            elif method == 3:
                #generate x,y coordinates that cover all boxes
                for x in range(9):
                    y = x*3 - (8* (x//3))
                    self.claim_col(x, y)
 
            elif method == 4:
                #generate x coordinates that cover all rows
                for x in range(9):
                    self.box_row(x)
 
            elif method == 5:
                #generate y coordinates that cover all columns
                for y in range(9):
                    self.box_col(y)
             
            elif method == 6:
                #generate x,y coordinates that cover all boxes, rows and columns
                for x in range(9):
                    y = x*3 - (8* (x//3))
                    self.hidden_twins(x, y)
                     
            elif method == 7:
                #generate x,y coordinates that cover all boxes, rows and columns
                for x in range(9):
                    y = x*3 - (8* (x//3))
                    self.naked_twins(x, y)
            
            #recursively change the original sudoku slightly, and create a new Grid to solve it
            else:
                minimumOptions = [10, None, None]
                for x in range(9):
                    for y in range(9):
                        if len(self.gridList[x][y].possibilities) != 1:
                            if len(self.gridList[x][y].possibilities) < minimumOptions[0]:
                                minimumOptions = [len(self.gridList[x][y].possibilities), x, y]
            
                for a in range(minimumOptions[0]):
                    newSudoku = self.build_sudoku()
                    x = minimumOptions[1]
                    y = minimumOptions[2]
                    newSudoku[x] = newSudoku[x][:y] + str(self.gridList[x][y].possibilities[a]) + newSudoku[x][y+1:]
                    newGrid = Grid(newSudoku)
                    if newGrid.solve():
                        self.gridList = newGrid.gridList
                        break
                    
                
                                            
            statusAfter = self.get_progress()
            #if the operation hasn't been successful
            if statusAfter >= statusBefore:
                method += 1
                #if the methods have been exhausted
                if method == 9:
                    working = False
            else:
                print(method)
                method = 0
        
        #enable recursion
        if self.is_solved():
            return True
        else:
            return False

    #remove possibilities from squares based on certain values           
    def reduce_possibilities(self,x,y):

        currentSquare = self.gridList[x][y]
        
        impactSet = self.get_impactSet(x, y)
        for impactSquare in impactSet:
            if impactSquare.certain():
                currentSquare.remove_pos(impactSquare.value())
    
    #assign a value if it is the only workable value for a row, column or box
    def assign_place(self,x,y):
        box = self.get_box(x,y)
        row = self.get_row(x)
        col = self.get_col(y)
        impactList = [box,row,col]
        for group in impactList:
            for num in range(1,10):
                possibleList = []
                for square in group:
                    if num in square.possibilities:
                        possibleList.append(square)
                if len(possibleList) == 1:
                    if len(possibleList[0].possibilities) != 1:
                        possibleList[0].possibilities = [num]

    #remove a number from a row if it must be in a certain box
    def claim_row(self,x,y):
        box = self.get_box(x,y)
        for num in range(1,10):
            rowSet = set()
            for square in box:
                if num in square.possibilities:
                    rowSet.add(square.x)
            if len(rowSet) == 1:
                row = rowSet.pop()
                for square in self.get_row(row):
                    if square not in box:
                        square.remove_pos(num)

    #remove a number from a column if it must be in a certain box
    def claim_col(self,x,y):
        box = self.get_box(x,y)
        for num in range(1,10):
            colSet = set()
            for square in box:
                if num in square.possibilities:
                    colSet.add(square.y)
            if len(colSet) == 1:
                col = colSet.pop()
                for square in self.get_col(col):
                    if square not in box:
                        square.remove_pos(num)    

    #remove a number from part of a box if it must be in a certain row
    def box_row(self,x):
        rowSquares = self.get_row(x)
        boxSet = set()
        for num in range(1,10):
            for square in rowSquares:
                if num in square.possibilities:
                    boxSet.add(square.y//3)
            if len(boxSet) == 1:
                boxX = (x//3) * 3
                boxY = boxSet.pop() * 3
                for row in range(boxX, boxX + 3):
                    for col in range(boxY, boxY + 3):
                        square = self.gridList[row][col]
                        if square not in rowSquares:
                            square.remove_pos(num)

    #remove a number from part of a box if it must be in a certain column          
    def box_col(self,y):
        colSquares = self.get_col(y)
        boxSet = set()
        for num in range(1,10):
            for square in colSquares:
                if num in square.possibilities:
                    boxSet.add(square.x//3)
            if len(boxSet) == 1:
                boxX = boxSet.pop() * 3
                boxY = (y//3) * 3
                for row in range(boxX, boxX + 3):
                    for col in range(boxY, boxY + 3):
                        square = self.gridList[row][col]
                        if square not in colSquares:
                            square.remove_pos(num)

    def hidden_twins(self,x,y):
        box = self.get_box(x,y)
        row = self.get_row(x)
        col = self.get_col(y)
        impactList = [box,row,col]
        for group in impactList:
            twinList = []
            for num in range(1,10):
                twinList.append([])
                for square in group:
                    if num in square.possibilities:
                        twinList[-1].append(square)
                        
            for i1 in range(9):
                for i2 in range(i1+1, 9):
                    if twinList[i1] == twinList[i2] and len(twinList[i1]) == 2:
                        num1 = i1+1
                        num2 = i2+1
                        for square in group:
                            if square not in twinList[i1]:
                                square.remove_pos(num1)
                                square.remove_pos(num2)
    
    def naked_twins(self,x,y):
        box = self.get_box(x,y)
        row = self.get_row(x)
        col = self.get_col(y)
        impactList = [box,row,col]
        for group in impactList:
            for i1 in range(9):
                for i2 in range(i1+1, 9):
                    if group[i1].possibilities == group[i2].possibilities and len(group[i1].possibilities) == 2:
                        num1 = group[i1].possibilities[0]
                        num2 = group[i1].possibilities[1]
                        for i3 in range(9):
                            if i3 != i2 and i3 != i1:
                                group[i3].remove_pos(num1)
                                group[i3].remove_pos(num2)


    def display(self):
        display = ''
        for x in range(9):
            for y in range(9):
                square = self.gridList[x][y]
                if y in [3,6]:
                    display +=' | '
                if square.certain():
                    display += str(square.value()) + ' '
                else:
                    display += ('0 ')
            if x in [2,5]:
                display += '\n-------+-------+-------\n'
            else:
                display += '\n'
        print(display)       
        
    def display_pos(self):
        display = ''
        for x in range(9):
            for y in range(9):
                square = self.gridList[x][y]
                if y in [3,6]:
                    display +=' | '
                display += str(len(square.possibilities)) + (' ')
            if x in [2,5]:
                display += '\n-------+-------+-------\n'
            else:
                display += '\n'
        print(display)          
           
    def build_sudoku(self):
        sudoku = []
        for x in range(9):
            sudoku.append('000000000')
            for y in range(9):
                if len(self.gridList[x][y].possibilities) == 1:
                    sudoku[x] = sudoku[x][:y] + str(self.gridList[x][y].possibilities[0]) + sudoku[x][y+1:]
        return sudoku

        
if __name__ == '__main__':
    
    #hardest
    #originalSudoku = ['800000000','003600000','070090200','050007000','000045700','000100030','001000068','008500010','090000400']
    
    #supposedly hard
    originalSudoku = ['006008500','000070613','000000009','000090001','001000800','400530000','107053000','050064000','300100060']
    
    #blank
    #originalSudoku = ['000000000' for a in range(9)]
       
    #very hard
    #originalSudoku = ['010600300','500030018','020500000','300000020','000704000','090000007','000006070','150090002','006003050']
    
    #medium/hard
    #originalSudoku = ['002000430','003065000','000008000','900000200','080000050','007000003','000400000','000980300','056000700']
    
    #hard
    #originalSudoku = ['000300260','007008010','006020000','050000071','000094008','000000000','530000000','000106580','090200000']
    
    #no solution for this below one
    #originalSudoku = ['790000300','000006900','800020076','000005002','005418700','400700000','610090008','002300000','009000054']
    #very easy - doable with only reduction of possibilities
    #originalSudoku = ['051200090','038079040','290500006','123600700','870301054','009008361','400002015','010860430','060007920']
    #easy
    #originalSudoku = ['020178030','040302090','100000006','008603500','300000004','006709200','900000002','080901060','010436050']
    g = Grid(originalSudoku)
    g.display()
    g.solve()
    g.display()
    print(g.is_solved())
    