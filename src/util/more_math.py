import math

def nearest_power_of_2(x):
	return math.pow(2, math.ceil(math.log2(x)))