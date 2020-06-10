import math

class calculos:
	def cDistance(x1, y1, x2, y2):
		dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
		return(dist)

	def ReLu(z):
		if z < 0:
			return(0.0)
		else:
			return(1.0)

	def tanh(z):
		a = (math.exp(z))-(math.exp(-z))
		b = (math.exp(z))+(math.exp(-z))
		return(a/b)

	def sigmoid(z):
		return(1/(1+math.exp(-z)))
	
	def sumatory(weigths, IN, bias, r):
		z = 0
		for i in range(r):
			z = z+(weigths[i]*IN[i])
		z = z+bias
		return(z)
		