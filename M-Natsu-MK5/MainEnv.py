from pyglet.gl import *
from PreForms import*
import random as rnd
from pyglet.window import key

class Window(pyglet.window.Window):
	def __init__(self):
		super().__init__(700,900)
		pyglet.clock.schedule_interval(self.update, 1/60)
		self.change = 0
		
		self.info = labelF('TEST', 8, self.height+128, "Coder's Crux", 15, 'left', 'center')
		self.info2 = labelF('TEST', 8, self.height+96, "Coder's Crux", 15, 'left', 'center')
		self.info3 = labelF('TEST', 8, self.height+64, "Coder's Crux", 15, 'left', 'center')
		self.info4 = labelF('TEST', 8, self.height+32, "Coder's Crux", 15, 'left', 'center')

		self.finishp = triangleF(self.width/2, self.height-32, 32, 32)
		self.finishp.color(230, 75, 120)
		self.gen        = 0
		self.square 	= []
		self.startP 	= 50
		self.deadP 		= 0
		self.dt_finishl = 0

		self.fitness 	 = 0
		self.bestFitness = 0

		self.weights 	= []
		self.biases 	= []
		self.rWeights 	= []
		self.rBiases 	= []

		self.rgb 		= []
		self.bestRgb 	= []
		self.rRgb 		= []

		self.bestWeights 	= []
		self.bestBiases 	= []

		self.mutation	= 10

		self.layers 	= 3
		self.rows 		= 4

		self.solid = squareS(self.width/2, self.height/2, 400, 32)

		self.startPop()

		self.lineL = lineF(1, self.height, 1, 0, 2)
		self.lineR = lineF(self.width, self.height, self.width, 0, 2)
		self.lineD = lineF(0,0, self.width, 0, 2)
		self.lineU = lineF(0,self.height, self.width, self.height, 2)

		self.outlines 	= []
		self.neuron 	= []
		self.inputs 	= []
		self.outputs 	= []
		self.outs 		= [] 
		self.ins 		= []
		self.lweights	= []
		self.cweights	= []
		self.cneurons	= []
		self.sbiases	= []
		self.cbiases	= []
		self.lbiases 	= []
		self.xoff = 0
		self.yoff = 0
		self.top = 0

		self.offtime = 0
		self.drawN = 0

		self.draw_net()
	def draw_net(self):
		self.xx = (self.width/2)-60
		self.yy = self.height
		self.xoff = 64
		self.yoff = 32
		self.outlines = []
		if self.top != self.layers:
			for j in range(self.rows):
				for i in range(self.layers+2):
					self.outlines.append(squareS(self.xx+(self.xoff*i), self.yy-(self.yoff*j)+(self.yoff*self.rows), 18, 18))

			for i in range(self.layers):
				self.outlines.append(squareS(self.xx+(self.xoff*i)+self.xoff/3, self.yy+(self.yoff*self.rows)+self.yoff/2, 10, 10))
				self.sbiases.append(squareS(self.xx+(self.xoff*i)+self.xoff/3, self.yy+(self.yoff*self.rows)+self.yoff/2, 8, 8))
				self.lbiases.append([])

				for j in range(self.rows):
					self.lbiases[i].append(lineF(self.xx+(self.xoff*i)+self.xoff/3, self.yy+(self.yoff*self.rows)+self.yoff/2, \
						(self.xx+(self.xoff*i)+self.xoff/3)+self.xoff/1.5, self.yy+(self.yoff*j)+self.yoff, 2))

			for i in range(self.layers):
				self.lweights.append([])
				for j in range(self.rows):
					self.lweights[i].append([])
					for k in range(self.rows):
						self.lweights[i][j].append(lineF(self.xx+(self.xoff*i), self.yy-(self.yoff*j)+(self.yoff*self.rows),\
						 self.xx+(self.xoff*i)+64, self.yy-(self.yoff*k)+(self.yoff*self.rows), 1))
			for i in range(self.rows):
				self.neuron.append([])
				self.inputs.append(squareS(self.xx, self.yy-(self.yoff*i)+(self.yoff*self.rows), 16, 16))
				self.outputs.append(squareS(self.xx+(self.xoff*self.layers)+self.xoff,\
				 self.yy-(self.yoff*i)+(self.yoff*self.rows), 16, 16))
				for j in range(self.layers):
					self.neuron[i].append(squareS(self.xx+(self.xoff*j)+64,\
					 self.yy-(self.yoff*i)+(self.yoff*self.rows), 16, 16))

		for i in range(self.layers):
			if self.cbiases != []:
				if self.cbiases != 0:
					if self.cbiases[i] > 0:
						self.sbiases[i].color(0, round(255/self.cbiases[i]), round(185/self.cbiases[i]))
					elif self.cbiases[i] < 0:
						self.sbiases[i].color(round(255/self.cbiases[i]), 0, round(185/self.cbiases[i]))
				else:
					self.sbiases[i].color(0, 0, 0)		


		for i in range(self.layers):
			for j in range(self.rows):
				for k in range(self.rows):
					if self.cweights != []:
					 	if self.cweights[i][j][k] != 0:
						 	if self.cweights[i][j][k] > 0:
						 		self.lweights[i][j][k].color(0, round(255/(self.cweights[i][j][k])), 120)
						 	elif self.cweights[i][j][k]  < 0:
						 		self.lweights[i][j][k].color(round(255/(self.cweights[i][j][k])), 0, 120)
					 	else:
					 		self.lweights[i][j][k].color(0, 0, 0)

		for i in range(self.rows):
			self.inputs[i].color(75, 190, 230)
			self.outputs[i].color(230, 190, 75)
			for j in range(self.layers):
				self.neuron[i][j].color(25, 32, 4)

		self.top = self.layers
		self.drawN = 1

	def startPop(self):
		
		for i in range(self.startP):
			self.square.append(squareF(350, 64, 16, 16, 700, 900, 0, 0, 0, self.layers, self.rows))
			self.square[i].color(rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255))

	def newPop(self):
		for i in range(self.startP-1):
			self.DNAC()
			self.square.append(squareF(350, 64, 16, 16, 700, 900, 1, self.weights, self.biases, self.layers, self.rows))
			self.weights = self.rWeights[:]
			self.biases = self.rBiases[:]
			self.square[i].color(self.rgb[0], self.rgb[1], self.rgb[2])
			self.rgb = self.rRgb[:]
		self.square.append(squareF(350, 64, 16, 16, 700, 900, 1, self.bestWeights, self.bestBiases, self.layers, self.rows))
		self.square[self.startP-1].color(self.bestRgb[0], self.bestRgb[1], self.bestRgb[2])

	def update(self, dt):
		if self.square[self.startP-1].finish == 1:
			self.mutation = 5
		for i in range(len(self.square)):
			if self.fitness < self.square[i].fitness:
				self.dt_finishl = self.square[i].dtf
				self.fitness = self.square[i].fitness

				self.biases = self.square[i].biases[:]
				self.weights = self.square[i].weights[:]
				self.cweights = self.weights[:]
				self.rgb = self.square[i].rgb[:]
				self.cbiases = self.square[i].Net.biases[:]


			self.square[i].update()  
			if self.square[i].alive == 0:
				self.deadP += 1
		if self.offtime >= 0 and self.offtime < 2:
			self.offtime += 1
		elif self.offtime == 2:
			self.offtime = 3
			if self.drawN == 1:
				self.draw_net()


		if self.deadP < self.startP:
			self.deadP = 0
		else:
			self.deadP = 0
			self.clearWin()


		self.info.update('Distance:'+str(self.dt_finishl))
		self.info2.update('fitness 	  :'+str(self.fitness))
		self.info3.update('bestFitness:'+str(self.bestFitness))
		self.info4.update('Gen:'+str(self.gen))

		if self.drawN == 1:
			self.outs = self.square[self.startP-1].outputs[:]
			self.ins = self.square[self.startP-1].inputs[:]
			for i in range(self.layers):
				self.cneurons.append([])
				for j in range(self.rows):
					self.cneurons[i].append(self.square[self.startP-1].Net.neurons[i][j].r)

			if self.outs != [] and self.cneurons != []:
				for i in range(self.rows):
					if self.ins[i] != 0:
						if self.ins[i] > 0:
							self.inputs[i].color(round(200/self.ins[i]), 75, round(255/self.ins[i]))
						elif self.ins[i] < 0:
							self.inputs[i].color(round(200/self.ins[i]), 75, 0)
						else:
							self.inputs[i].color(0, 75, 0)


					if self.outs[i] == 0:
						self.outputs[i].color(0,0,0)
					else:
						self.outputs[i].color(230, 19, 75)
					for j in range(self.layers):
						if self.cneurons[j][i] != 0:
							if self.cneurons[j][i] > 0:
								self.neuron[i][j].color(round(125/-self.cneurons[j][i]), round(255/self.cneurons[j][i]), 75)
							elif self.cneurons[j][i] < 0:
								self.neuron[i][j].color(round(255/self.cneurons[j][i]), round(125/-self.cneurons[j][i]), 75)
							else:
								self.neuron[i][j].color(0, 0, 75)
			self.cneurons = []

	def DNAC(self):
		if self.fitness > self.bestFitness:
			self.bestFitness = self.fitness
			self.bestWeights = self.weights[:]
			self.bestBiases = self.biases[:]
			self.bestRgb = self.rgb[:]
			self.cweights = self.bestWeights[:]
			if self.drawN == 1:
				self.draw_net()
			for i in range(self.layers):
				self.bestWeights[i] = self.bestWeights[i][:]
				for j in range(4):
					self.bestWeights[i][j] = self.bestWeights[i][j][:]

		self.rBiases = self.bestBiases[:]
		self.rWeights = self.bestWeights[:]
		for i in range(self.layers):
			self.rWeights[i] = self.rWeights[i][:]
			for j in range(4):
				self.rWeights[i][j] = self.rWeights[i][j][:]

		for i in range(self.layers):
			self.biases[i] += rnd.randint(-self.mutation, self.mutation)/100
			self.weights[i] = self.weights[i][:]
			for j in range(4):
				self.weights[i][j] = self.weights[i][j][:]
				for k in range(4):
					self.weights[i][j][k] += rnd.randint(-self.mutation, self.mutation)/100
		self.rRgb = self.rgb[:]
		for i in range(3):
			if self.rgb[i] > 255:
				self.rgb[i] = self.rgb[i]-255
			elif self.rgb[i] < 0:
				self.rgb[i] = self.rgb[i]+255
			self.rgb[i] = min(self.rgb[i] + rnd.randint(-20, 20), 255)

	def on_draw(self):
		self.clear()
		fBatch.draw()
		fps_display.draw()

	def clearWin(self):
		for i in range(self.startP):
			pass
		if self.square:
			for i in range(len(self.square)):
				self.square[i].clean()
			self.square.clear()
		self.square = []
		self.gen = self.gen+1
		self.newPop()
		self.dt_finishl = 0
		self.fitness = 0
		self.weights = []
		self.biases = []

	def restartWin(self):
		if self.square:
			for i in range(len(self.square)):
				self.square[i].clean()
			self.square.clear()
		self.square = []
		self.startPop()
		self.dt_finishl = 0
		self.bestFitness = 0
		self.fitness = 0
		self.weights = []
		self.biases = []
		self.bestBiases = 0
		self.bestWeights = 0
		self.rWeights = 0
		self.rBiases = 0
		self.bestFitness
		self.gen = 0
		self.offtime = 0


if __name__ == '__main__':
	window = Window()
	@window.event
	def on_key_press(symbol, modifiers):
			if symbol == key.R:
				window.restartWin()
	fps_display = pyglet.window.FPSDisplay(window=window)
	pyglet.app.run()