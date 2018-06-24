'''
Created on 15 Apr 2018

@author: George
'''
import numpy as np
import pickle
import gzip


class NeuralNet(object):

    def __init__(self):
        self.nodeList = []
        self.weights = []
        self.deltaWeights = []
        
    def train(self, epochs, inputs, outputs, learningRate, hiddenNodeStructure):
        self.nodeList = [inputs.shape[1]] + hiddenNodeStructure + [outputs.shape[1]]
        
        decayRate = learningRate / epochs / 2
        
        self.set_up_weights()
        self.set_up_deltaWeights()
        
        for n in range(1,epochs+1):
        
            #forward propagation
            layerList = self.forward_propagation(inputs)
        
            #backward propagation
            self.backward_propagation(outputs, layerList, learningRate)
            
            learningRate -= decayRate
        
            if n % 10000 == 0:
                print(n, self.weights)
                
            if n % 1000 == 0:
                print(n, '\n desired output:\n', outputs, '\nactual output:\n',  layerList[-1],'\ndifference:\n', outputs - layerList[-1])        
    

    def predict(self, inputs):
        outputs = self.forward_propagation(inputs)
        return outputs[-1]
    
    def store(self, fileName):
        for index in range(len(self.weights)):
            self.weights[index] = (self.weights[index]).tolist()
        string = str(self.nodeList) + '!!!' + str(self.weights)
        print(string)
        
        file = open('C:\\Users\\George\\Documents\\Computing\\Python files\\sudoku solver stuff\\' + fileName + '.txt', 'w')
        file.write(string)
        file.close()
        
        #algorithm to store the weights (and/or node structure) in a text file goes here
        
    def load(self, fileName):
        file = open(fileName, 'r')
        fileString = file.read()
        file.close()
        fileList = fileString.split('!!!')
        self.nodeList = eval(fileList[0])
        self.weights = eval(fileList[1])
        for index in range(len(self.weights)):
            self.weights[index] = np.array(self.weights[index])
        
        #algorithm to extract the weights (and/or node structure) from a text file goes here
    
    def activation(self, num):
        return 1 / ( (np.exp(-num) ) + 1)
    
    def dactivation(self, num):
        return self.activation(num) * self.activation(1 - (num))
    
    def set_up_weights(self):
        self.weights = []
        for i in range(1, len(self.nodeList)):
            row = self.nodeList[i-1]
            col = self.nodeList[i]
            self.weights.append(2*np.random.random((row, col)) - 1)
    
    def set_up_deltaWeights(self):
        self.deltaWeights = [np.zeros(self.weights[a].shape) for a in range(len(self.weights))]
    
    def forward_propagation(self, inputs):
        layerList = [inputs]
        for i in range(len(self.nodeList) - 1):
            layerList.append(self.activation(np.dot(layerList[i],self.weights[i])))
        return layerList
    
    def backward_propagation(self, outputs, layerList, learningRate):
        #find the difference between the intended and actual results
        resultDifference = outputs - layerList[-1]
    
        slopeOutput = self.dactivation(layerList[-1])
        self.deltaWeights[-1] = resultDifference * slopeOutput
        
        for i in range(len(self.nodeList)-3, -1, -1):
            slopeHidden = self.dactivation(layerList[i+1])
        
            hiddenError = np.dot(self.deltaWeights[i+1], np.transpose(self.weights[i+1]))
            self.deltaWeights[i] = hiddenError * slopeHidden
        
        for i in range(len(self.nodeList)-1):
            self.weights[i] += np.dot(np.transpose(layerList[i]), self.deltaWeights[i]) * learningRate


#===============================================================================
# inputs = np.array([[0,0,1],
#                    [0,1,0],
#                    [1,0,1],
#                    [1,1,1]])
# 
# outputs = np.array([[0],
#                     [1],
#                     [1],
#                     [0]])
#===============================================================================

def generate_training_data(dataFile, labelFile):
    with open(dataFile, "br") as file:
        print(file.readable())
        dataContents = file.read()
        print(len(dataContents)/(28*28))
         
    with open(labelFile, "br") as file:
        print(file.readable())
        labelContents = file.read()
        

    return data





NN = NeuralNet()

dataFile = "C:\\Users\\George\\Documents\\Computing\\Python files\\sudoku solver stuff\\training_data\\t10k-images-idx3-ubyte.gz"
labelFile = "C:\\Users\\George\\Documents\\Computing\\Python files\\sudoku solver stuff\\training_data\\t10k-labels-idx1-ubyte.gz"

inputs, outputs = generate_training_data(dataFile, labelFile)

NN.train(60000, inputs, outputs, 0.3, [30])
  
print(NN.predict(inputs))
  
NN.store('a')

#loading
NN.load('C:\\Users\\George\\Documents\\Computing\\Python files\\sudoku solver stuff\\a.txt')
    
print(NN.predict(inputs))



