import time

name = "Amplifier"
vers = "0.0.0"

old_time = None

def disp(*values: object):
	print(f"[{name}-{vers}]", " ".join(map(str, values)))

def stage_finish(*values: object):
	global old_time

	new_time = time.time()
	elapsed = (new_time - old_time) if old_time else 0
	print(f"[{name}-{vers}]", *values, f"[{elapsed:.1f}s]")
	old_time = new_time

# TODO use rich to build cool panels in the console!
	# TODO don't use global variables (in future it would be nice to have multiple models on the same process)

	# TODO active queries
	# TODO memory usage statistics
	# TODO graph statistics
	# TODO problem solving progress over time
	# TODO memory access graph
		# use matplotlib to produce locations for all the points
			# strengths is access correlation
			# initial position is average depth to access in a ring
		# truncate to integer positions on a grid
		# flash when accessed, slowly diminish over time
