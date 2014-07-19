__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-07-19"
__version__	= "0.0.2"
__license__ = "Creative Commons Attribution-NonCommercial 3.0 License."

import os
import yaml

import cherrypy

import copy

import tools.text.mako_render as mako_render
import tools.text.xml_render as xml_render


import sys
import traceback

"""	
	def pushText(self,name):
		try:
			base_name=self.Path+name+'.'
			if os.path.isfile(base_name+'_xml'):
				self.currentPage=xml_render.TextRender(self,name)
				txt=self.currentPage.render()
			elif os.path.isfile(base_name+'mako'):
				self.currentPage=mako_render.TextRender(self,name)
				txt=self.currentPage.render()

			if self.WebSocket:
				self.ws_send('message',txt)
				
		except Exception as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
			exception_str=''.join('!! ' + line for line in lines)
			print(exception_str)
"""
			


class Story_with_Websocket():
	WebSocket=None
	msgQueue=None
	
	def __init__(self):
		self.msgQueue=[]
	def ws_receive(self,msg_type,msg_data):
		if msg_type=='greeting':
			self.handleGreeting(msg_data)
		elif msg_type=='message':
			if msg_data[0]=='action':
				self.handleAction(msg_data[1],msg_data[2])

	def ws_send(self,msg_type,msg_data):
		if self.WebSocket:
			self.WebSocket.sendJS(msg_type,msg_data)
			while len(self.msgQueue):
				msg=self.msgQueue.pop()
				self.WebSocket.sendJS(msg[0],msg[1])
		else:
			self.msgQueue.append([msg_type,msg_data])

			
	def raiseEvent(self,event_type,data):
		self.ws_send('event',[event_type,data])
	
	def pushText(self,data):
		self.ws_send('message',['text',data])
	
	def pushPageState(self,prop,data):
		self.ws_send('message',['page::'+prop,data])

	def pushEvent(self,txt):
		if self.WebSocket:
			self.ws_send('event',txt)

	def handleAction(self,action,data):
		print("(Story_with_Websocket) action",action,data)
		
class StoryObject():
	Story=None
	Data=None
	def __init__(self,story,data):
		self.Story=story
		self.Data=data

class Character(StoryObject):
	def __init__(self,story,data):
		StoryObject.__init__(self,story,data)
		
		if not 'location' in self.Data:
			self.Data['location']='__unknown__'
			
		if not 'visits' in self.Data:
			self.Data['visits']={}

		if not 'ActionCount' in self.Data:
			self.Data['ActionCount']={}
		
	def moveToRoom(self,room):
		if room != self.Data['location']:
			if room in self.Data['visits']:
				self.Data['visits'][room]=self.Data['visits'][room]+1
			else:
				self.Data['visits'][room]=1
			self.Data['location']=room

	def moveToDirection(self,direction):
		room=self.Data['location']
		if room in self.Story.Rooms:
			directions=self.Story.Rooms[room]['directions']
			if direction in directions:
				new_room=directions[direction]
				if new_room in self.Story.Rooms:
					self.moveToRoom(new_room)
	
	def doAction(self,object_type,object_id,action):
		ident=object_type+'::'+object_id+'.'+action
		
		if not ident in self.Data['ActionCount']:
			self.Data['ActionCount'][ident]=0
		else:
			self.Data['ActionCount'][ident]=self.Data['ActionCount'][ident]+1
		
		if object_type=='room':
			text_path='rooms/'
		else:
			text_path=object_type+'/'
			
		if self.Story.loadPage(text_path+object_id+'.'+action):
			self.Story.showPage()

class Player(Character):
	def __init__(self,story,data):
		Character.__init__(self,story,data)
		
		self.manageMove(self.Data['location'])
		
	def moveToRoom(self,room):
		Character.moveToRoom(self,room)
		self.manageMove(room)
		
	def manageMove(self,room):
		if room in self.Story.Rooms:
			self.Story.pushRoomInfo(room)
			
			if self.Story.loadPage('rooms/'+room):
				self.Story.showPage(
					visits=self.Data['visits'][room]
				)
		else:
			#unknown room
			#now what?
			print("Room '%s' not known!"%room)
		
class Story_PushEvents:
	def New(self):
		cherrypy.log("A new story has been started...")
		self.pushEvent('story::new')
		self.loadPage('new')
		self.showPage()
		self.loadData(copy.deepcopy(self.DefaultData))
		self.Data['is_new']=False
		
	def PostLoad(self):
		self.pushEvent('Story.PostLoad')
		
	def Exit(self):
		cherrypy.log("Exiting... ")
		self.pushEvent('story::exit')
		self.WebSocket.terminate()
		self.WebSocket=None

	def pushRoomInfo(self,room_name):
		print(self.Rooms[room_name])
		self.ws_send(
			'message',
			['room::info',self.Rooms[room_name]]
		)

class Story(Story_with_Websocket,Story_PushEvents):
	Path=None
	story_id=None
	Data=None
	DefaultData=None
	Rooms=None
	Player=None
	active=False
	currentPage=None
	PageStack=None
	ManagerThread=None
	
	def __init__(self,story_id,story_data,default_data,path):
		Story_with_Websocket.__init__(self)
		
		self.story_id=story_id
		self.DefaultData=default_data
		self.Path=path
		self.PageStack={}
		self.loadRooms()
		self.loadData(story_data)

	def dumpData(self):
		self.Data['Player']=self.Player.Data
		
		return self.Data
	
	def loadData(self,new_data):
		self.PageStack={}
		self.Data=new_data
		if not 'Player' in self.Data:
			self.Data['Player']={}
		self.Player=Player(self,self.Data['Player'])
		self.PostLoad()
		
	def loadRooms(self):
		self.Rooms={}
		try:
			yaml_file=os.path.join(self.Path,'rooms.yaml')
			if os.path.isfile(yaml_file):
				data=yaml.load(file(yaml_file,'r'))
				for cRoom in data['rooms']:
					self.Rooms[cRoom]=data['rooms'][cRoom]
				for cRoom in data['room-map']:
					self.Rooms[cRoom]['directions']={}
					for cDir in data['room-map'][cRoom]:
						target_room=data['room-map'][cRoom][cDir]
						if	 ('hidden' in self.Rooms[target_room]) and self.Rooms[target_room]['hidden']: 
							pass
						else:
							self.Rooms[cRoom]['directions'][cDir]=data['room-map'][cRoom][cDir]
			
		except Exception as e:
			print("Error:",e)
		print(self.Rooms)


	def loadPage(self,page_name):
		try:
			base_name=os.path.join(self.Path,page_name+'.')
			if os.path.isfile(base_name+'_xml'):
				self.currentPage=xml_render.PageRender(self,page_name)
				return True
			elif os.path.isfile(base_name+'mako'):
				self.currentPage=mako_render.PageRender(self,page_name)
				return True
		except Exception as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
			exception_str=''.join('!! ' + line for line in lines)
			print(exception_str)

	def showPage(self,**args):
		try:
			txt=self.currentPage.render(**args)
			if self.WebSocket:
				self.pushText(txt)
				self.pushPageState('done',self.currentPage.Done)
				
		except Exception as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
			exception_str=''.join('!! ' + line for line in lines)
			print(exception_str)
	
	def handleGreeting(self,data=None):
		self.active=True
		cherrypy.log("Got greeting from client...")
		if self.Data['is_new']:
			self.New()
		if self.Player:
			self.Player.manageMove(self.Player.Data['location'])
		if self.currentPage:
			self.pushPageState('done',self.currentPage.Done)


	def handleEvent(self,data=None):
		print("(Story) event",data)

	def handleAction(self,action,data):
		if action=='Page.nextSection':
			self.currentPage.nextSection()
			self.showPage()
		elif action=='Player.moveToDirection':
			self.Player.moveToDirection(data)
		elif action=='Room.action':
			self.Player.doAction('room',self.Player.Data['location'],data)
			
		print("(Story) action",action,data)
		
	def handleClose(self,data=None):
		print("(Story) close",data)
	
	def manage(self):
		if self.active:
			if not 'i' in self.Data:
				self.Data['i']=0
				
			if not self.Data['is_new']:
				print("manage of story: %s" %self.story_id)
				if self.WebSocket:
					#self.send(simplejson.dumps(response), False)
					#self.pushText('Data["i"] = '+ str(self.Data['i'])+'/'+str(id(self)))
					#self.Data['i']=self.Data['i']+1
					#cherrypy.log(str(self.i))
					pass
