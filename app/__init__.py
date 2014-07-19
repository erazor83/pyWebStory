__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-07-19"
__version__	= "0.2.0"
__license__ = "Creative Commons Attribution-NonCommercial 3.0 License."

"""
Main app and URL-handlers
includes
  * websocket
  * json-RPC
  
"""

PYWEBGAME_PATHS = None

import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

import cherrypy
import simplejson
import time

from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=[current_dir+'/data/pages/'])

from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

import sys
sys.path.append('lamegame_cherrypy_authority/')

import lg_authority

import os

import urlparse

import app.tools.story as story_tools
import app.tools.user as user_tools
import threading
import select

import traceback
WEBSOCKET_DETAILS={}

def postImport():
	story_tools.PYWEBGAME_PATHS = PYWEBGAME_PATHS
	user_tools.PYWEBGAME_PATHS = PYWEBGAME_PATHS
	
	
	story_tools.STORY_DATA_LOCK=threading.RLock()
	story_tools.STORY_DATA={}
	story_tools.DEFAULT_STORY_DATA={}
	story_tools.STORY_INSTANCES={}
	story_tools.postImport()
	
	user_tools.USER_DATA_LOCK=threading.RLock()
	user_tools.USER_DATA={}
	user_tools.postImport()
	

class TPL_Helpers():
	def _getJSFromView(self,view_name):
		"""get a list of .js files which are located in js/<view_name>/"""
		if view_name=='':
			url_path='index'
		else:
			url_path=view_name
		
		js_folder=os.path.join('js',url_path)
		full_js_folder=os.path.join(PYWEBGAME_PATHS['app_data'],js_folder)
		ret=[]
		if os.path.exists(full_js_folder):
			for cFile in os.listdir(full_js_folder):
				extension = os.path.splitext(cFile)[1]
				if extension=='.js':
					ret.append(os.path.join(self.base_path,js_folder,cFile))
		return ret

	def _getCSSFromView(self,view_name):
		"""get a list of .css files which are located in js/<view_name>/"""
		if view_name=='':
			url_path='index'
		else:
			url_path=view_name
		
		css_folder=os.path.join('css',url_path)
		full_css_folder=os.path.join(PYWEBGAME_PATHS['app_data'],css_folder)
		ret=[]
		if os.path.exists(full_css_folder):
			for cFile in os.listdir(full_css_folder):
				extension = os.path.splitext(cFile)[1]
				if extension=='.css':
					ret.append(os.path.join(self.base_path,css_folder,cFile))
		return ret

	def _getJSFromStory(self,story_id):
		"""get a list of .js files which are located in js/<view_name>/"""
		
		full_js_folder=os.path.join(story_tools.STORY_PATHS[story_id],'js')
		ret=[]
		if os.path.exists(full_js_folder):
			for cFile in os.listdir(full_js_folder):
				extension = os.path.splitext(cFile)[1]
				if extension=='.js':
					ret.append(os.path.join(self.base_path,'story',story_id,'js',cFile))
		return ret

	def _getCSSFromStory(self,story_id):
		"""get a list of .js files which are located in js/<view_name>/"""
		
		full_css_folder=os.path.join(story_tools.STORY_PATHS[story_id],'css')
		ret=[]
		if os.path.exists(full_css_folder):
			for cFile in os.listdir(full_css_folder):
				extension = os.path.splitext(cFile)[1]
				if extension=='.css':
					ret.append(os.path.join(self.base_path,'story',story_id,'css',cFile))
		return ret
	
	
	
@lg_authority.groups('auth')
class JSON_RPC(object):
	auth = lg_authority.AuthRoot()
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def index(self,*args, **kwargs):
		rpc_uri=cherrypy.request.params.get('uri')
		rpc_method=cherrypy.request.params.get('do')
		if not rpc_method:
			rpc_method='read'
		
		if rpc_method=='read':
			pass
		else:
			raise cherrypy.HTTPError(404)
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def me(self,*args, **kwargs):
		rpc_uri=cherrypy.request.params.get('uri')
		rpc_method=cherrypy.request.params.get('do')
		if not rpc_method:
			rpc_method='get'
		user_id=cherrypy.user.id
		if rpc_method=='get':
			if		rpc_uri == 'last_story':
				return user_tools.getLastStory()
			elif	rpc_uri == 'valid_stories':
				return story_tools.listStories()
			elif	rpc_uri == 'last_saved_stories':
				ret={}
				saves=user_tools.listSavedStories(user_id,None)
				for story_id in saves:
					for save_name in saves[story_id]:
						if not story_id in ret:
							ret[story_id]=saves[story_id][save_name]
						elif ret[story_id]['time']<saves[story_id][save_name]['time']:
							ret[story_id]=saves[story_id][save_name]
				return ret
			elif	rpc_uri == 'saved_stories':
				if 'story' in kwargs:
					story_id=kwargs['story']
				else:
					story_id=None
				return user_tools.listSavedStories(user_id,story_id)
			
			elif	rpc_uri == 'story_saves':
				story_id=kwargs['story']
				return user_tools.getStorySaves(user_id,story_id)
			elif	rpc_uri == 'dump_worldState':
				return story_tools.getStoryData(user_id,kwargs['story'])

		elif rpc_method=='quicksave_story':
			story_id=kwargs['story']
			return story_tools.saveStory(user_id,story_id,'__quicksave__')
		elif rpc_method=='quickload_story':
			story_id=kwargs['story']
			return story_tools.loadStory(user_id,story_id,'__quicksave__')

		elif rpc_method=='save_story':
			story_id=kwargs['story']
			save_name=kwargs['name']
			return story_tools.saveStory(user_id,story_id,save_name)
		elif rpc_method=='load_story':
			story_id=kwargs['story']
			save_name=kwargs['name']
			return story_tools.loadStory(user_id,story_id,save_name)

		elif rpc_method=='delete_save':
			story_id=kwargs['story']
			save_name=kwargs['name']
			
		elif rpc_method=='new_story':
			story_id=kwargs['story']
			s_instance_key=user_id+'.'+story_id
			story_tools.STORY_INSTANCES[s_instance_key].New()
			return True
		elif rpc_method=='exit_story':
			story_id=kwargs['story']
			s_instance_key=user_id+'.'+story_id
			story_tools.STORY_INSTANCES[s_instance_key].Exit()
			return True
		else:
			raise cherrypy.HTTPError(404)
		
def Auth_Render(*args,**kwargs):
	cherrypy.log(str(args))
	cherrypy.log(str(kwargs))
	return ""

class WS_handler(WebSocket):
	user_id=None
	Story=None
	msg_idx=0
	socket_ident=None
	
	def opened(self):
		self.QS=urlparse.parse_qs(self.environ['QUERY_STRING'])
		self.socket_id=self.QS['id'][0]
		
		if self.socket_id in WEBSOCKET_DETAILS:
			self.user_id=WEBSOCKET_DETAILS[self.socket_id]['user_id']
			self.Story=WEBSOCKET_DETAILS[self.socket_id]['story']
			self.Story.WebSocket=self
			"""
			if self.Story.ManagerThread and self.Story.ManagerThread.isAlive():
				self.Story.ManagerThread.stop()
				self.Story.ManagerThread._Thread__stop()
			"""
			if not self.Story.ManagerThread:
				self.Story.ManagerThread=story_tools.Manager(self.Story)
				self.Story.ManagerThread.start()
				cherrypy.engine.subscribe('stop',self.Story.ManagerThread.stop)
		else:
			self.user_id=None
			

		"""
		s = self.stream
		try:
			self.opened()
			sock = self.sock
			fileno = sock.fileno()
			process = self.process
			
			while not self.terminated:
				ready_to_read, ready_to_write, in_error = select.select(
					[sock],
					[],
					[sock],
					1
				)
				if len(ready_to_read):
					rxbytes = ready_to_read[0].recv(self.reading_buffer_size)
					if not process(rxbytes):
						break
				if self.Story:
					self.Story.manage()
		finally:
			self.client_terminated = self.server_terminated = True
							
		try:
			if not s.closing:
				self.closed(1006, "Going away")
			else:
				self.closed(s.closing.code, s.closing.reason)
		finally:
			s = sock = fileno = process = None
			self.close_connection()
			self._cleanup()
		"""

	def received_message(self, message):
		parsed_message=simplejson.loads(message.data)
		
		cherrypy.log("ws receive %s"%str(message))
		self.msg_idx=parsed_message['id']
		
		if parsed_message['socket'] != self.socket_id:
			self.socket_id=None
			cherrypy.log("Invalid socket-id received!")
		
		if not self.user_id:
			cherrypy.log("No user for websocket!")
			
		if not self.Story:
			cherrypy.log("No Story for websocket!")
			
		if (not self.user_id) or (not self.Story) or (not self.socket_id):
			self.sendJS('message',['err','invalid_session'])
			time.sleep(1)
			self.close()
		else:
			try:
				self.Story.ws_receive(parsed_message['type'],parsed_message['data'])
			except Exception:
				exc_type, exc_value, exc_traceback = sys.exc_info()
				lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
				exception_str=''.join('!! ' + line for line in lines)
				print(exception_str)
		
	def sendJS(self,msg_type,msg_data):
		self.msg_idx=self.msg_idx+1
		msg={
			'id':self.msg_idx,
			'socket':self.socket_id,
			'type':msg_type,
			'data':msg_data,
			'reply':False
		}
		self.send(simplejson.dumps(msg), False)

	def closed(self, code, reason="A client left the room without a proper explanation."):
		if self.socket_id in WEBSOCKET_DETAILS:
			del WEBSOCKET_DETAILS[self.socket_id]
		if self.Story:
			self.Story.handleClose()
			self.Story.WebSocket=None
			if self.Story.ManagerThread and self.Story.ManagerThread.isAlive():
				self.Story.ManagerThread.stop()
				self.Story.ManagerThread._Thread__stop()
				self.Story.ManagerThread=None
		cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))

@lg_authority.groups('auth')
class Root(object,TPL_Helpers):
	base_path='/'
	auth = lg_authority.AuthRoot()
    
	def __init__(self):
		#self.scheme = 'wss' if ssl else 'ws'
		pass
	
	@cherrypy.expose
	def index(self,*args,**kwargs):
		tmpl = lookup.get_template("index.mako")
		
		if not 'do' in kwargs:
			if len(args)==0:
				view_name='index'
			else:
				view_name=args[0]
			return tmpl.render(
				js_path=os.path.join(self.base_path,"js",''),
				css_path=os.path.join(self.base_path,"css",''),
				ws_path=os.path.join(self.base_path,"ws",''),
				base_path=self.base_path,
				user_id=cherrypy.user.id,
				user_name=cherrypy.user.name,
				js_files=self._getJSFromView(view_name),
				css_files=self._getCSSFromView(view_name)
			)
		else:
			do=kwargs['do']
			if 'story' in kwargs:
				if do=='new':
					story_id=kwargs['story']
					story_tools.newStoryInstance(cherrypy.user.id,story_id)
					raise cherrypy.HTTPRedirect(os.path.join(self.base_path,'story',story_id,''))
				elif do=='load_story':
					story_id=kwargs['story']
					save_name=kwargs['name']
					loaded=story_tools.loadStory(cherrypy.user.id,story_id,save_name)
					if loaded==True:
						raise cherrypy.HTTPRedirect(os.path.join(self.base_path,'story',story_id,''))
					else:
						raise cherrypy.HTTPError(400)
				
				else:
					raise cherrypy.HTTPError(501)
			else:
				raise cherrypy.HTTPError(400)

	@cherrypy.expose
	def story(self,*args,**kwargs):
		if len(args)>=1:
			story_id=args[0]
			if story_id in story_tools.STORY_INFO:
				if len(args)==1:
					if cherrypy.request.path_info[-1]!='/':
						#story has to be called as a path
						raise cherrypy.HTTPRedirect(os.path.join(self.base_path,'story',story_id,''))
					if not story_tools.getStoryData(cherrypy.user.id,story_id):
						raise cherrypy.HTTPRedirect(self.base_path)
					view_name='story'
					tmpl = lookup.get_template("story.mako")
					
					#todo: this will hold story defined js files
					story_js_files=self._getJSFromStory(story_id)

					#todo: this will hold story defined css files
					story_css_files=self._getCSSFromStory(story_id)
					
					return tmpl.render(
						js_path=os.path.join(self.base_path,"js",''),
						css_path=os.path.join(self.base_path,"css",''),
						ws_path=os.path.join(self.base_path,"ws",''),
						base_path=self.base_path,
						story_id=story_id,
						story_info=story_tools.STORY_INFO[story_id],
						user_id=cherrypy.user.id,
						user_name=cherrypy.user.name,
						js_files=self._getJSFromView(view_name)+story_js_files,
						css_files=self._getCSSFromView(view_name)+story_css_files
					)
				else:
					if args[1] in ['images','js','css']:
						path='/'.join(args[1:])
						
						#make sure no one tries to go out of allowed path
						paths=[story_tools.STORY_PATHS[story_id]]+list(args[1:])
						base_dir = os.path.realpath(os.path.join(*paths))
						
						paths=[story_tools.STORY_PATHS[story_id]]+list(args[1:])
						final_path = os.path.join(*paths)
						
						if os.path.isfile(final_path) and os.path.commonprefix([base_dir, final_path]) == base_dir:
							return cherrypy.lib.static.serve_file(final_path)
					
		raise cherrypy.HTTPError(404)

	@cherrypy.expose
	def ws(self,*args, **kwargs):
		s_instance_key=cherrypy.user.id+'.'+args[0]
		if s_instance_key in story_tools.STORY_INSTANCES:
			WEBSOCKET_DETAILS[kwargs['id']]={
				'user_id'		:cherrypy.user.id,
				't_created'	:time.time(),
				'story_id'	:args[0],
				'story'			:story_tools.STORY_INSTANCES[s_instance_key]
			}
