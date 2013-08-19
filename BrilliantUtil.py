#!/usr/local/bin/python3
### Utility Functions for BrilliantTest ###

import os, sys, inspect

def ImportAlgorithm(name):
	filename = "algorithms/" + name
	path = list(sys.path)
	dirTup = os.path.split(filename)
	directory = dirTup[0]
	sys.path.insert(0, directory)
	module_name = dirTup[1]
	try:
		module = __import__(module_name)
		del sys.modules[name]
	except:
		module = os
	finally:
		sys.path[:] = path # restore
	
	return module

def Validate(item):
	try:
		# Check Hunting Function
		l = item.hunt_choices(1, 3000, 0, 5, [0 for x in range(11)])
		assert(len(l) == 11)

		# Check Hunting Outcomes
		item.hunt_outcomes([0 for x in range(11)])

		# Check Round End
		item.round_end(0, 5, 11)

		return l
	except:
		for c in inspect.getmembers(item, inspect.isclass):
			try:
				d = c[1]()
				# Check Hunting Function
				l = d.hunt_choices(1, 3000, 0, 5, [0 for x in range(11)])
				assert(len(l) == 11)

				# Check Hunting Outcomes
				d.hunt_outcomes([0 for x in range(11)])

				# Check Round End
				d.round_end(0, 5, 11)

				return c[1]
			except:
				pass
		return False