#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-02-16"
__version__	= "0.0.1"
__license__ = "Creative Commons Attribution-NonCommercial 3.0 License."

"""
	we need:
	  * simplejson
	  * pycherry
	  * ws4py
	  * pyyaml

"""
import os.path

PYWEBGAME_PATHS ={
	'root'				:os.path.dirname(os.path.abspath(__file__))+'/',
	'stories'			:os.path.dirname(os.path.abspath(__file__))+'/data/stories/',
	'app_data'		:os.path.dirname(os.path.abspath(__file__))+'/app/data/',
	'story_saves'	:os.path.dirname(os.path.abspath(__file__))+'/data/saves/',
}

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
	cherrypy.config.update(
		{
			'environment': 				'production',
			'log.error_file':			'site.log',
			'server.socket_host':	'0.0.0.0',
			'server.socket_port':	8088,
			'engine.autoreload.on':True,
			'log.screen': 				True,

			'tools.lg_authority.on': True, 
			# Uncomment the following two lines to persist changed user / group data
			'tools.lg_authority.site_registration': 'email',
			'tools.lg_authority.site_storage': 			'sqlite3', 
			'tools.lg_authority.site_storage_conf': {'file': 'auth.db'},
			'tools.lg_authority.site_template_dir':	'app/data/pages/auth/',
			'tools.lg_authority.site_email': {
					'smtpserver': 'erazor-zone.de',
					'smtpport': 25,
					'smtpssl': False,
					'smtpuser': 'web1p1',
					'smtppass': 'XXX',
					'default': 'Site <test@example.com>'
			}

		}
	)

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
	
