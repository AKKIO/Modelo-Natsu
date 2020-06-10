from pyglet.gl import*
import random as rnd
from calculations import *
from NeuralNet import *
class setUp:
	batch = pyglet.graphics.Batch()

class squareF:
	def __init__(self, x, y, width, height, ww, wh, startN, weights, biases, layers, rows):

		self.rgb = [255,255,255]
		self.x, self.y = x/width, y/height
		self.width, self.height = width, height
		self.ww, self.wh = ww, wh

		self.life = 200
		self.spd = 0.5
		self.cspd = 0
		self.fitness = 0
		self.dtf = 0
		self.weights = []
		self.biases = []

		self.inputs = []
		self.outputs = []
		self.finish = 0

		self.alive = 1
		self.vertex_list = 0;
		self.define()
		self.inputs_outputs()
		self.Net = NeuralNetwork(layers, rows)

		if startN == 0:
			self.Net.startNet()
		else:
			self.weights = weights
			self.biases = biases
			self.Net.newNet(self.weights, self.biases)

	def inputs_outputs(self):
		for i in range(4):
			self.inputs.append(0)

	def color(self, r, g, b):
		self.rgb = [r,g,b]

	def process(self):
		self.dtf = calculos.cDistance(self.x*self.width, self.y*self.height, self.ww/2, self.wh-32)
		return self.dtf

	def define(self):
		self.coords = (	self.x*self.width-(self.width/2),	self.y*self.height-(self.height/2),	0.0, 
						self.x*self.width+(self.width/2),	self.y*self.height-(self.height/2),	0.0, 
						self.x*self.width+(self.width/2),	self.y*self.height+(self.height/2),	0.0, 
					   	self.x*self.width-(self.width/2),	self.y*self.height+(self.height/2),	0.0)
		self.vertex_list = setUp.batch.add(4, GL_QUADS, None,('v3f', self.coords),('c3B', self.rgb*4))

	def update(self):
		if self.alive == 1:
			self.cspd = self.spd
			self.life -= 1
			self.vertex_list.delete()
			self.define()
			self.process()

			self.weights = self.Net.weights[:]
			self.biases = self.Net.biases[:]

			self.inputs[0] = self.cspd
			self.inputs[1] = self.dtf/100
			self.inputs[2] = self.x/10
			self.inputs[3] = self.y/10

			self.Net.update(self.inputs)
			self.outputs = self.Net.outputs[:]
			self.movement()

			if self.y > ((self.wh/2)-16)/self.height and self.y < ((self.wh/2)+16)/self.height:
				if self.x > ((self.ww/2)-200)/self.width and self.x < ((self.wh/2)+200)/self.width:
					self.dead()

			if self.x >= self.ww/self.width or self.x < 0 or self.y >= self.wh/self.height or self.y <= 0:
				self.dead()
			if self.dtf <= 16:
				self.finish = 1
				self.dead()
			if self.life <= 0:
				self.dead()
			self.fitness = 1.0/(self.dtf * self.dtf)

	def dead(self):
		self.alive = 0

	def movement(self):
		if self.outputs[0] == 1:
			self.y += self.spd
		if self.outputs[1] == 1:
			self.x += self.spd
		if self.outputs[2] == 1:
			self.y -= self.spd
		if self.outputs[3] == 1:
			self.x -= self.spd


	def clean(self):
		self.vertex_list.delete()

class lineF:
	def __init__(self, x1, y1, x2, y2, sz):
		self.rgb = [255,255,255]
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.sz = sz
		self.vertex_list = 0;
		self.define()

	def color(self, r, g, b):
		self.rgb = [r,g,b]
		self.define()

	def update(self):
		self.vertex_list.delete()
		self.define()

	def define(self):
		self.coords = (self.x1,self.y1,0, self.x2,self.y2,0)
		self.vertex_list = setUp.batch.add(2,GL_LINES, None, ('v3f', self.coords), ('c3B', self.rgb*2))
		glLineWidth(self.sz)

class squareS:
	def __init__(self, x, y, width, height):

		self.rgb = [255,255,255]
		self.x, self.y = x/width, y/height
		self.width, self.height = width, height
		self.vertex_list = 0;
		self.define()

	def color(self, r, g, b):
		self.rgb = [r,g,b]
		self.define()

	def define(self):
		self.coords = (	self.x*self.width-(self.width/2),	self.y*self.height-(self.height/2),	0.0, 
						self.x*self.width+(self.width/2),	self.y*self.height-(self.height/2),	0.0, 
						self.x*self.width+(self.width/2),	self.y*self.height+(self.height/2),	0.0, 
					   	self.x*self.width-(self.width/2),	self.y*self.height+(self.height/2),	0.0)
		self.vertex_list = setUp.batch.add(4, GL_QUADS, None,('v3f', self.coords),('c3B', self.rgb*4))

	def update(self):
		self.vertex_list.delete()
		self.define()

	def clean(self):
		self.vertex_list.delete()
		
class triangleF:
	def __init__(self, x, y, width, height):
		self.rgb = (255,255,255, 255,255,255, 255,255,255)
		self.x = x/width
		self.y = y/height
		self.width = width
		self.height = height
		self.vertex_list = 0;
		self.define()

	def color(self, r, g, b):
		self.rgb = (r,g,b, r,g,b, r,g,b)
		self.define()

	def define(self):
		self.coords = (	self.x*self.width-(self.width/2),	self.y*self.height-(self.height/2),	0.0, 
						self.x*self.width+(self.width/2),	self.y*self.height-(self.height/2),	0.0, 
						self.x*self.width,					self.y*self.height+(self.height/2),	0.0)
		self.vertex_list = setUp.batch.add(3, GL_TRIANGLES, None,('v3f', self.coords),('c3B', self.rgb))

class labelF:
	def __init__(self, text, x, y, font, sz, ax, ay):
		self.text = text
		self.font = font
		self.sz = sz
		self.x = x
		self.y = y
		self.ax = ax
		self.ay = ay
		self.etiqueta = pyglet.text.Label(self.text, font_name=self.font, font_size=self.sz, x=self.x,y=self.y,anchor_x = self.ax, anchor_y = self.ay, batch = setUp.batch)

	def update(self, new_text):
		self.etiqueta.delete()
		self.text = new_text
		self.etiqueta = pyglet.text.Label(self.text, font_name=self.font, font_size=self.sz, x=self.x,y=self.y,anchor_x = self.ax, anchor_y = self.ay, batch = setUp.batch)

class fBatch:
	def draw():
		setUp.batch.draw()
