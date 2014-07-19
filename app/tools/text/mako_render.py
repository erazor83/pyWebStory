__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-03-11"
__version__	= "0.1.0"
__license__ = "Creative Commons Attribution-NonCommercial 3.0 License."

from mako.template import Template
from mako.lookup import TemplateLookup

class PageRender():
	Story=None
	Pagename=None
	Sections=None
	Section=None
	Done=True
	sectionIDX=None
	
	def __init__(self,story,filename):
		self.Pagename=filename
		self.Story=story
		self.TPL_Lookup=TemplateLookup(
			directories=[story.Path]
		)
		self.sectionIDX=0

	def nextSection(self):
		if self.sectionIDX<(len(self.Sections)-1):
			self.sectionIDX=self.sectionIDX+1
			self.Section=self.Sections[self.sectionIDX]

	def render(self,**kwargs):
		if not kwargs:
			kwargs={}
		tmpl = self.TPL_Lookup.get_template(
			self.Pagename+'.mako'
		)
		kwargs['Page']=self
		kwargs['StoryData']=self.Story.Data
		kwargs['Rooms']=self.Story.Rooms
		kwargs['me']=self.Story.Player
		#print(self.Story.Player.Data)
		kwargs['myActionCount']=self.Story.Player.Data['ActionCount']
		txt=tmpl.render(**kwargs)
		if self.Sections:
			if not self.Section:
				self.sectionIDX=0
				self.Section=self.Sections[0]
				#we need to rerender the page
				txt=tmpl.render(**kwargs)
			if self.Section==self.Sections[-1]:
				self.Done=True
			else:
				self.Done=False
		else:
			self.Done=True
		return txt