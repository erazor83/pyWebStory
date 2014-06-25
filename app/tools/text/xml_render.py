__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-03-11"
__version__	= "0.1.0"
__license__ = "Creative Commons Attribution-NonCommercial 3.0 License."

import os

try:
	from lxml import etree
except ImportError:
	try:
		# Python 2.5
		import xml.etree.cElementTree as etree
	except ImportError:
		try:
			# Python 2.5
			import xml.etree.ElementTree as etree
		except ImportError:
			try:
				# normal cElementTree install
				import cElementTree as etree
			except ImportError:
				try:
					# normal ElementTree install
					import elementtree.ElementTree as etree
				except ImportError:
					print("Failed to import ElementTree from any known place")

def parsePYWS_XML(xml_file):
	ret=[]
	if os.path.isfile(xml_file):
		xml_tree = etree.parse(xml_file)
		for element in xml_tree.getroot():
			print(element.tag)
			
class PageRender():
	pass