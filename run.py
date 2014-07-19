#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-07-19"
__version__	= "0.1.0"
__license__ = "Creative Commons Attribution-NonCommercial 3.0 License."

"""
	we need:
	  * simplejson
	  * pycherry
	  * ws4py
	  * pyyaml
	  * my version of lamegame_cherrypy_authority
"""
import os.path

ROOT_PATH=os.path.dirname(os.path.abspath(__file__))
PYWEBGAME_PATHS ={
	'root'				:ROOT_PATH,
	'conf'				:os.path.join(ROOT_PATH,'conf'),
	'stories'			:os.path.join(ROOT_PATH,'data','stories'),
	'app_data'		:os.path.join(ROOT_PATH,'app','data'),
	'story_saves'	:os.path.join(ROOT_PATH,'data','saves'),
}

import yaml
import cherrypy

import app


from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket

import sys
sys.path.append('lamegame_cherrypy_authority/')
import lg_authority

def _inheritGlobals():
	app.PYWEBGAME_PATHS=PYWEBGAME_PATHS
	
	app.postImport()
	
if __name__ == '__main__':
	
	_inheritGlobals()
	
	# Set up site-wide config first so we get a log if errors occur.
	conf=yaml.load(file(os.path.join(PYWEBGAME_PATHS['conf'],'default.yaml'),'r'))
	cherrypy.config.update(conf)

	#check if we have a local config
	local_conf=os.path.join(PYWEBGAME_PATHS['conf'],'local.yaml')
	if os.path.isfile(local_conf):
		conf=yaml.load(file(local_conf,'r'))
		cherrypy.config.update(conf)
		
	WebSocketPlugin(cherrypy.engine).subscribe()
	cherrypy.tools.websocket = WebSocketTool()
 
	conf = {
		'/feed': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join(PYWEBGAME_PATHS['root'], 'feeds'),
			'tools.staticdir.content_types': {
				'rss': 'application/xml',
				'atom': 'application/atom+xml'
			}
		},
		'/images':  {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join(PYWEBGAME_PATHS['root'], 'app/data/images/'),
		},
		'/js':  {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join(PYWEBGAME_PATHS['root'], 'app/data/js/'),
		},
		'/css':  {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': os.path.join(PYWEBGAME_PATHS['root'], 'app/data/css/'),
		},
		'/ws': {
			'tools.websocket.on': True,
			'tools.websocket.handler_cls': app.WS_handler
		}
	}
	
	rpc_conf = {
		'/rpc': {
			# the api uses restful method dispatching
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),

			# all api calls require that the client passes HTTP basic authentication
			'tools.authorize.on': True,
		}
	}

	cherrypy.tree.mount(app.Root(), '/', config=conf)
	cherrypy.tree.mount(app.JSON_RPC(), '/rpc', config=rpc_conf)
					
	cherrypy.engine.start()
	cherrypy.engine.block()
