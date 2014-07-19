"""
	some additional dict helpers
"""

__author__  = """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__    = "2014-06-19"
__version__ = "0.1.0"
__credits__ = """Copyright e-design, Alexander Krause <alexander.krause@ed-solutions.de>"""

from copy import deepcopy

def merge(a, b):
	if not isinstance(b, dict):
		return b
	result = deepcopy(a)
	for k, v in b.iteritems():
		if k in result and isinstance(result[k], dict):
			result[k] = merge(result[k], v)
		else:
			result[k] = deepcopy(v)
	return result
