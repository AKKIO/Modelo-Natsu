import random as rnd
import datetime
from calculations import *

class NeuralNetwork:
	def __init__(self, layers, rows):
		self.layers 	= layers
		self.rows 		= rows
		self.weights 	= []

		self.inputs 	= [0] * self.rows
		self.neurons 	= []
		self.biases 	= []
		self.outputs 	= [0] * self.rows

	def startNet(self):
		for i in range(self.layers):
			self.biases.append(rnd.randint(-10, 10)/ 10)
		for i in range(self.layers):
			self.weights.append([])
			for j in range(self.rows):
				self.weights[i].append([])
				for k in range(self.rows):
					self.weights[i][j].append(rnd.randint(-10, 10)/10)
		self.startNeurons()

	def newNet(self, weights, biases):
		self.biases = biases
		self.weights = weights
		self.startNeurons()

	def startNeurons(self):
		for i in range(self.layers):
			self.neurons.append([])
			for j in range(self.rows):
				self.neurons[i].append(Neuron(self.weights[i][j], self.inputs, self.biases[i], [i,j]))


	def update(self, inputs):
		self.upinputs = inputs
		self.neurons[0][0].inputs = self.upinputs
		self.neurons[0][1].inputs = self.upinputs
		self.neurons[0][2].inputs = self.upinputs
		self.neurons[0][3].inputs = self.upinputs
		for i in range(self.layers):
			for j in range(4):
				self.neurons[i][j].update()
			if i < self.layers-1:
				self.neurons[i+1][0].inputs[0] = self.neurons[i][0].r
				self.neurons[i+1][1].inputs[1] = self.neurons[i][1].r
				self.neurons[i+1][2].inputs[2] = self.neurons[i][2].r
				self.neurons[i+1][3].inputs[3] = self.neurons[i][3].r
			else:
				self.outputs[0] = calculos.ReLu(self.neurons[i][0].r)
				self.outputs[1] = calculos.ReLu(self.neurons[i][1].r)
				self.outputs[2] = calculos.ReLu(self.neurons[i][2].r)
				self.outputs[3] = calculos.ReLu(self.neurons[i][3].r)



class Neuron:
	def __init__(self, weights, inputs, bias, ID):
		self.ID 	= ID
		self.bias 	= bias
		self.z	 	= 0
		self.inputs 	= inputs
		self.weights	= weights
		self.r 		= 0


	def update(self):
		self.z = calculos.sumatory(self.weights, self.inputs, self.bias, 4)
		self.r = calculos.tanh(self.z)




if __name__ == '__main__':
	NN = NeuralNetwork()