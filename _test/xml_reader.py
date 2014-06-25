import os.path
import sys

cPath=os.path.dirname(os.path.abspath(__file__))
sys.path.append(cPath+'/../app/')

import tools.text.xml_render

demo_xml_file=cPath+'/../data/stories/global/demo/new.xml'

print(tools.text.xml_render.parsePYWS_XML(demo_xml_file))