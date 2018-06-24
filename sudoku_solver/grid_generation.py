'''
Created on 15 Apr 2018

@author: George
'''
#recognising the board using Hough transformation

import numpy as np
import random
from PIL import Image, ImageFilter

class Process(object):
    def __init__(self, image):
        #comment  
        self.im = image
        self.original = image
        self.width = self.im.size[0]
        self.height = self.im.size[1]
        self.pixels = self.im.load()
        self.threshold = 50
        
    def preprocess(self):
        copy = self.im.copy()
        self.im = copy.convert('L').convert("RGB")
        self.pixels = self.im.load()
        for a in range(self.width):
            for b in range(self.height):
                if a == 0 or b == 0 or a == self.width - 1 or b == self.height -1:
                    self.pixels[(a,b)] = (0,0,0)
                elif not self.large_value(self.pixels[a,b]):
                    self.pixels[(a,b)] = (255,255,255)
                else:
                    self.pixels[(a,b)] = (0,0,0)

    #edit classes so this is called less frequently
    def find_edges(self):
        self.im = self.im.filter(ImageFilter.FIND_EDGES)
        self.pixels = self.im.load()
        for a in range(self.width):
            for b in range(self.height):
                if a == 0 or b == 0 or a == self.width - 1 or b == self.height -1:
                    self.pixels[(a,b)] = (0,0,0)
                elif self.large_value(self.pixels[a,b]):
                    self.pixels[(a,b)] = (255,255,255)
                else:
                    self.pixels[(a,b)] = (0,0,0)

    def large_value(self, tup):
        if tup[0] > self.threshold or tup[1] > self.threshold or tup[2] > self.threshold:
            return True
        return False

class FindLines(Process):

    def __init__(self, image, accuracy = 100):
        Process.__init__(self, image)
        
        self.angleRes = accuracy
        self.diagonal = int(np.sqrt(self.height**2 + self.width**2))
        
        #set up a table of rho values against theta values, to represent the possible lines in the image
        self.rhos = np.arange(-self.diagonal, self.diagonal)
        self.thetas = np.arange(-np.pi/2, np.pi/2, np.pi/self.angleRes)
        self.acc = [[0 for a in range(len(self.thetas))] for b in range(len(self.rhos))]
        self.lineList = []

    def get_lines(self, edges = True):
        if edges:
            self.find_edges()
        else:
            self.preprocess()
        self.fill_accumulator()
        self.find_lines(50)

        self.draw_lines()
        self.show_image()
        
    def fill_accumulator(self):
        self.pixels = self.im.load()
        for x in range(self.width):
            for y in range(self.height):
                if random.random() > 0:
                    if self.large_value(self.pixels[(x,y)]): 
                        self.pixels[(x,y)] = (255,0,0)
                        for theta in range(len(self.thetas)):
                            angle = self.thetas[theta]
                            rho = int(round(x * np.cos(angle) + y * np.sin(angle)))
                            rhoIndex = (np.where(self.rhos == rho))[0][0]
                            self.acc[rhoIndex][theta] += 1

    def find_lines(self, number = 20): 
        for rho in range(len(self.rhos)):
            for theta in range(len(self.thetas)):
                self.lineList.append((rho,theta))

        self.lineList = self.sort_lines_by_acc()
        if number < len(self.lineList):
            self.lineList = self.lineList[:number]

        for i in range(len(self.lineList)):
            self.lineList[i] = (self.rhos[self.lineList[i][0]], self.thetas[self.lineList[i][1]] )

    def sort_lines_by_acc(self):
        accValue = []
        for rho in range(len(self.rhos)):
            for theta in range(len(self.thetas)):
                accValue.append(self.acc[rho][theta])

        return [x for _,x in sorted(zip(accValue,self.lineList))][::-1] 

    def find_angle(self):
        angles = [0 for a in range(self.angleRes)]
        for (rho, theta) in self.lineList:
            angle = int(self.angleRes * (0.5 - (theta / np.pi)))
            angles[angle % self.angleRes] += 1
            angles[(angle-1) % self.angleRes] += 1
            angles[(angle+1) % self.angleRes] += 1
            angles[(angle+self.angleRes//2 - 1) % self.angleRes] += 1
            angles[(angle+self.angleRes//2) % self.angleRes] += 1
            angles[(angle+self.angleRes//2 + 1) % self.angleRes] += 1            
        
        mainTheta = angles.index(max(angles))
        mainAngle = (np.pi/2) - ((mainTheta / self.angleRes) * np.pi )
        return np.rad2deg(mainAngle)

    def draw_lines(self):
        #lines = [(self.diagonal-500, 0)]
        for line in self.lineList:
            rho = line[0]
            angle = line[1]
            cosTheta = np.cos(angle)
            sinTheta = (np.sin(angle))
            if angle != 0:
                for x in range(self.width):
                    y = int(( rho - (x * cosTheta) ) / sinTheta)
                    if y > 0 and y < self.height-1:
                        self.pixels[(x,y) ] = (0,255,0)
                for y in range(self.height):
                    x = int(( rho - (y * sinTheta) ) / cosTheta)
                    if x > 0 and x < self.width-1:
                        self.pixels[(x,y) ] = (0,255,0)
            else:
                x =  int(rho)
                if x < self.width:
                    for y in range(0, self.height):
                        self.pixels[(x,y)] = (0,255,0)
            
    def show_image(self):
        self.im.show()

#calibrate this better
class LocateSquares(Process):
    
    def __init__(self, image):
        Process.__init__(self, image)
        self.find_edges()
        

    
    def get_corners(self):
        res = 50
        paraThetas = [a*np.pi/res for a in range(-2, 3, 1)]
        perpThetas = [(np.pi/2 - a*np.pi/res) for a in range(2)] + [(-np.pi/2 + a*np.pi/res) for a in range(2)]
        
        cornerLim = 0
        found = False
            
        paraLines = self.get_lineList(paraThetas, res)

        perpLines = self.get_lineList(perpThetas, res)
        
        predictedSize = self.predict_size(paraLines, perpLines)
        inter = self.get_intersections(paraLines, perpLines, predictedSize)
        print(len(inter))

        topCornerList = self.find_key_corner_list(inter, paraLines, perpLines, True)

        bottomCornerList = self.find_key_corner_list(inter, paraLines, perpLines, False)
        
        if len(topCornerList) > cornerLim and len(bottomCornerList) > cornerLim:
            found = True
        
        if found:
            print(found)
            topCornerList = self.score_corners_by_neighbours(topCornerList, True)
            bottomCornerList = self.score_corners_by_neighbours(bottomCornerList, False)
            
            pair = self.choose_corner_pair(topCornerList, bottomCornerList,  paraLines, perpLines, predictedSize)
            
            if pair != []:
                x1,y1 = pair[1]
                x2,y2 = pair[2]
                keyLines = pair[3]
                minorAngle = self.get_minor_angle(keyLines, paraLines, perpLines)
                self.show_corners(x1,y1)
                self.show_corners(x2,y2)
                self.im.show()
                
                print(x1,y1)
                print(x2,y2)
                x1,y1 = self.convert_coords_with_angle(x1, y1, minorAngle)
                x2,y2 = self.convert_coords_with_angle(x2, y2, minorAngle)
            
            else:
                found = False
        
        if not found:
            return []
        else:
            return np.rad2deg(minorAngle), (x1,y1,x2,y2)
            #return some kind of flag that the corners haven't been found

    def convert_coords_with_angle(self, x,y, angle):
        print(np.cos(angle), np.sin(angle), angle)
        x1 = round((x) * np.cos(angle) - (y) * np.sin(angle))
        y1 = round((y) * np.cos(angle) + (x) * np.sin(angle))
        return x1,y1
        

    def get_minor_angle(self, lines, paraLines, perpLines):
        a1,a2,a3,a4 = paraLines[lines[0]][1], perpLines[lines[1]][1], paraLines[lines[2]][1], perpLines[lines[3]][1]
        print(a1,a2,a3,a4)
        if a2 < 0:
            a2 += np.pi/2
        elif a2 > 0:
            a2 -= np.pi/2
        if a4 < 0:
            a4 += np.pi/2
        elif a4 > 0:
            a4 -= np.pi/2        
        
        minorAngle = (a1 + a2 + a3 + a4) / 4
        print(minorAngle)
        return -minorAngle
        

    def get_lineList(self, thetas, res):
        finder = FindLines(self.original.copy(), res)
        finder.thetas = np.array(thetas)
        finder.acc = [[0 for a in range(len(finder.thetas))] for b in range(len(finder.rhos))]
        
        finder.get_lines(True)
        lines = finder.lineList
        for i in range(len(lines)):
            rho = lines[i][0]
            rhoIndex = np.where(finder.rhos == rho)[0][0]

            angle = lines[i][1]
            theta = thetas.index(angle)

            accValue = finder.acc[rhoIndex][theta]

            lines[i] = (lines[i][0], lines[i][1], accValue)
        
        return lines

    def get_intersections(self, paraLines, perpLines, predictedSize):
        inter = []
        scores = []
        for i in range(len(paraLines)):
            for j in range(len(perpLines)):
                line1 = paraLines[i]
                line2 = perpLines[j]

                x,y = self.get_int_point(line1,line2)
                
                gapsX = self.count_lines_at_coord(y, paraLines, predictedSize//9)
                gapsY = self.count_lines_at_coord(x, perpLines, predictedSize//9)
                
                strength = line1[2] + line2[2] + gapsX + gapsY
                scores.append(strength)
                inter.append((0,x,y,i,j))

        scores = self.normalise_scores(scores)
        
        for i in range(len(paraLines)*len(perpLines)):
            inter[i] = (scores[i]*4, inter[i][1],inter[i][2],inter[i][3],inter[i][4])
        return sorted(inter)[::-1]
    
    def get_int_point(self, line1, line2):
        rho1 = line1[0]
        angle1 = line1[1]
        a,b,c = np.cos(angle1), np.sin(angle1), rho1
        
        rho2 = line2[0]
        angle2 = line2[1]
        d,e,f = np.cos(angle2), np.sin(angle2), rho2
        
        x = int((b*f - e*c) / (b*d - e*a))
        y = int((a*f - d*c)/(a*e  - d*b)) 
        return x,y
    
    def count_lines_at_coord(self, rho, lineList, gap):
        count = 0
        for line in lineList:
            for x in range(-20, 20):
                actualGap = abs(line[0] - rho*x)
                dif = abs(gap-actualGap)
                if dif < 5:
                    count += 1
        return count
    
    def normalise_scores(self, scoreList):
        maxScore = max(scoreList)
        for i in range(len(scoreList)):
            scoreList[i] /= maxScore
        return scoreList

    def consider_quad(self, points, direction):
        newPoints = []
        if direction:
            for i in range(len(points)):
                if points[i][1] < self.width //2 and points[i][2] < self.height //2:
                    newPoints.append(points[i])
        else:
            for i in range(len(points)):
                if points[i][1] > self.width //2 and points[i][2] > self.height //2:
                    newPoints.append(points[i])    
                           
        return newPoints

    
    def find_key_corner_list(self, inter, paraLines, perpLines, quad):
        countList = []
        lineWeight1 = []
        lineWeight2 = []
        inter = self.consider_quad(inter, quad)
        for corner in inter:
            x= corner[1]
            y= corner[2]
            line1 = paraLines[corner[3]]
            line2 = perpLines[corner[4]]
        
            count = self.count_points_on_lines(x,y,line1, line2, quad)
            countList.append(count)
            lineWeight1.append(line1[2])
            lineWeight2.append(line2[2])
        
        lineWeight1 = self.normalise_scores(lineWeight1)
        lineWeight2 = self.normalise_scores(lineWeight2)        
        
        if len(countList) == 0:
            return []
        countList = self.normalise_scores(countList)
        
        cornerList = []
        if len(countList) > 0:
            for i in range(len(countList)):
                cornerList.append((countList[i]+(lineWeight1[i]+lineWeight2[i])/5, inter[i][1], inter[i][2], inter[i][3], inter[i][4]))

        return sorted(cornerList)[::-1]

    def count_points_on_lines(self, x,y, paraLine, perpLine, forward):
        
        rho = paraLine[0]
        angle = paraLine[1]
        cosTheta = np.cos(angle)
        sinTheta = np.sin(angle)
        count1 = 0
        missed = 0
        while y < self.height-1 and y > 1 and missed < 5:
            x = round(( rho - (y * sinTheta) ) / cosTheta)
            if x > 0 and x < self.width-1:
                if self.large_value(self.pixels[(x-1,y)]) or self.large_value(self.pixels[(x,y)]) or self.large_value(self.pixels[(x+1,y)]):
                    count1 += 1
                    missed = 0
                else:
                    missed += 1
                    #self.pixels[(x,y)] = (255,255,0)
            if forward:
                y+=1
            else:
                y-=1
        
        if (y == 1 or y == self.height -1) and missed < 2:
            count1 = -1*count1


        rho = perpLine[0]
        angle = perpLine[1]
        cosTheta = np.cos(angle)
        sinTheta = np.sin(angle)
        count2 = 0
        missed = 0
        while x < self.width-1 and x > 1 and missed < 5:
            y = round(( rho - (x * cosTheta) ) / sinTheta)
            if y > 0 and y < self.height-1:
                if self.large_value(self.pixels[(x,y-1)]) or self.large_value(self.pixels[(x,y)]) or self.large_value(self.pixels[(x,y+1)]):
                    count2 += 1
                    missed = 0
                else:
                    missed += 1
                    #self.pixels[(x,y)] = (0,255,255)
            if forward:
                x+=1
            else:
                x-=1
        
        #disregard lines that reach the end of the image
        if (x == 1 or y == self.width -1) and missed < 2:
            count2 = -1*count2
    
        return count1+count2

    def score_corners_by_neighbours(self, cornerList, quad):
        total = 0
        for corner in cornerList:
            total += corner[0]
        scoreList = []
        for corner1 in cornerList:
            score = 0
            x1,y1 = corner1[1], corner1[2]
            for corner2 in cornerList:
                x2,y2 = corner2[1], corner2[2]
                if quad:     
                    if (x1 + 10 < x2 and abs(y2-y1) < 10) or (y1 + 10 < y2 and abs(x2-x1) < 10):
                        score += 1

                else:
                    if (x1 > x2 + 10 and abs(y2-y1) < 10) or (y1 > y2 + 10 and abs(x2-x1) < 10):
                        score += 1
            scoreList.append(score)
        
        scoreList = self.normalise_scores(scoreList)
        
        for i in range(len(cornerList)):
            cornerList[i] = ((scoreList[i] + cornerList[i][0])/2, cornerList[i][1], cornerList[i][2], cornerList[i][3], cornerList[i][4])
        return sorted(cornerList)


    def choose_corner_pair(self, topCorners, bottomCorners, paraLines, perpLines, predictedSize):
        cornerPairs = []
        sizeOffList = []
        pairQualityList = []
        ratioList = []
        print(len(topCorners), len(bottomCorners))
        topCorners, bottomCorners = self.filter_corners(topCorners), self.filter_corners(bottomCorners)
        print(len(topCorners), len(bottomCorners))
        #=======================================================================
        # for c in bottomCorners:
        #     self.show_corners(c[1], c[2])
        # self.im.show()
        #=======================================================================
        for c1 in topCorners:
            print(topCorners.index(c1))
            for c2 in bottomCorners:
                xSide = c2[1] - c1[1]
                ySide = c2[2] - c1[2]

                ratio = self.get_ratio(xSide, ySide)
                ratioList.append(ratio**3)
                
                
                sizeOff = self.get_size_off(predictedSize, xSide, ySide)
                sizeOffList.append(sizeOff)
                
                pairQuality = self.get_pair_quality(c1, c2, paraLines, perpLines) / 4
                
                pairQualityList.append(pairQuality)
                
                cornerPairs.append(((c1[0]+c2[0])/2, (c1[1], c1[2]), (c2[1], c2[2]), (c1[3], c1[4], c2[3], c2[4])))      
                
                  
        pairQualityList = self.normalise_scores(pairQualityList)
        sizeOffList = self.normalise_scores(sizeOffList)
        ratioList = self.normalise_scores(ratioList)
        
        for i in range(len(cornerPairs)):
            weight = (cornerPairs[i][0] * sizeOffList[i]**2 * pairQualityList[i]**6 * ratioList[i]**2)
            cornerPairs[i] = (weight, cornerPairs[i][1], cornerPairs[i][2], cornerPairs[i][3], (cornerPairs[i][0], sizeOffList[i], pairQualityList[i], ratioList[i]))
    
        cornerPairs = sorted(cornerPairs)[::-1]
        print(cornerPairs[0])

        self.im.show()
        #=======================================================================
        # for i in range(100):
        #     self.show_corners(cornerPairs[i][1][0], cornerPairs[i][1][1])
        #     self.show_corners(cornerPairs[i][2][0], cornerPairs[i][2][1])
        # self.im.show()
        #=======================================================================
        
        if len(cornerPairs) > 0:
            return cornerPairs[0]
        else:
            return []

    def filter_corners(self, corners):
        newCorners = []
        xys = []
        for c in corners:
            if (c[1],c[2]) not in xys:
                newCorners.append(c)
                for x in [c[1]-1, c[1], c[1] +1]:
                    for y in [c[2]-1, c[2], c[2] +1]:
                        xys.append((x,y))
        return newCorners

    def get_pair_quality(self, c1,c2, paraLines, perpLines):
        leftVer = paraLines[c1[3]]
        rightVer = paraLines[c2[3]]
        topHor = perpLines[c1[4]]
        bottomHor = perpLines[c2[4]]
        topRight = self.get_int_point(topHor, rightVer)
        bottomLeft = self.get_int_point(leftVer, bottomHor)
        topLeft = (c1[1], c1[2])
        bottomRight = (c2[1],c2[2])
        
        pairQuality = self.follow_line_from_A_to_B(topLeft, topRight, topHor, False)
        pairQuality += self.follow_line_from_A_to_B(topLeft, bottomLeft, leftVer, True)
        pairQuality += self.follow_line_from_A_to_B(topRight, bottomRight, rightVer, True)
        pairQuality += self.follow_line_from_A_to_B(bottomLeft, bottomRight, bottomHor, False)                
        
        return pairQuality

    def get_ratio(self,xSide, ySide):
        ratio = xSide / ySide
        if ratio >= 1:
            ratio = 1/ratio
            ratio = ratio
        return ratio

    def get_size_off(self, predictedSize, xSide, ySide):
        sizeOff = (xSide*ySide / predictedSize**2)**0.5
        return sizeOff

    def validate_coord(self, coord, maximum):
        if coord < 0:
            return 0
        if coord >= maximum:
            return maximum-1  
        return coord

    def follow_line_from_A_to_B(self, point1, point2, line, paraOrPerp):
        
        x1,y1 = point1[0], point1[1]
        x2,y2 = point2[0], point2[1]
        
        rho = line[0]
        angle = line[1]
        cosTheta = np.cos(angle)
        sinTheta = np.sin(angle)

        count = 0
        total = 1
        
        #para is vertical
        if paraOrPerp:
            y1, y2 = self.validate_coord(y1, self.height),self.validate_coord(y2, self.height)

            xNow, yNow = x2, y2

            while yNow > y1:
                xNow = round(( rho - (yNow * sinTheta) ) / cosTheta)
                if xNow < self.width-1 and xNow > 0:
                    if self.large_value(self.pixels[(xNow-1, yNow)]) or self.large_value(self.pixels[(xNow, yNow)]) or self.large_value(self.pixels[(xNow+1, yNow)]):
                        count += 1
                yNow -= 10
                total +=1            
        
        else:
            x1, x2 = self.validate_coord(x1, self.width),self.validate_coord(x2, self.width)        
            xNow, yNow = x2, y2

            while xNow > x1:
                yNow = round(( rho - (xNow * cosTheta) ) / sinTheta)
                if yNow < self.height-1 and yNow > 0:
                    if self.large_value(self.pixels[(xNow, yNow-1)]) or self.large_value(self.pixels[(xNow, yNow)]) or self.large_value(self.pixels[(xNow, yNow+1)]):
                        count +=1

                xNow -= 10
                total += 1

        #self.im.show()
        return count**3/total   

    def predict_size(self, lines1, lines2):
        if self.height > self.width:
            gapList = [0 for a in range(self.height+1)]
        else:
            gapList = [0 for a in range(self.width+1)]
            
        
        gapList = self.update_gapList(lines1, gapList)
        gapList = self.update_gapList(lines2, gapList)        
        
        
        newGapList = [0]
        for i in range(1, len(gapList)-1):
            tot = gapList[i-1] + gapList[i] + gapList[i+1]
            newGapList.append(tot)        
            
        newGapList = [0 for a in range(10)] + newGapList[10:]
        maxGap = newGapList.index(max(newGapList))
        
        return 500
        
        #size = maxGap * 9
        #return size
    
    def update_gapList(self, lines, gapList):
        newLines = []
        for l1 in lines:
            newLines.append(l1[0])
        newLines = sorted(newLines)
        for i in range(len(newLines)-1):
            gap = abs(newLines[i+1] - newLines[i])
            gapList[gap] += 1
        
        return gapList
    
    def show_corners(self, x, y):
        for x1 in range(x-1, x+2):
            for y1 in range(y-1, y+2):
                try:
                    self.pixels[(x1,y1)] = (255,0,255)
                except IndexError:
                    pass
    

