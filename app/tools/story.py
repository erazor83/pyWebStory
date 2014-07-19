__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-07-19"
__version__	= "0.0.2"
__license__ = "Creative Commons Attribution-NonCommercial 3.0 License."

"""
	helper tools for stories
"""

PYWEBGAME_PATHS = None

STORY_INSTANCES={}
STORY_INFO={}

STORY_PATHS={}
STORY_DATA_LOCK=None
STORY_DATA=None
DEFAULT_STORY_DATA=None

"""
def writeData(user,data)
    lock.acquire()
    try:
        if "foo" not in global_dict:
            global_dict["foo"] = 1
    finally:
        lock.release()
"""

import re

import os
import yaml
import simplejson
import cherrypy
import md5

import threading
#import sys
#sys.path.append('..')

import time

import app.base_story

class Manager(threading.Thread):
	_alive=False
	
	def __init__(self,story):
		threading.Thread.__init__(self)
		self.Story=story
		
	def run(self):
		self._alive=True
		while self.Story.WebSocket and self._alive:
			self.Story.manage()
			time.sleep(1)
			
	def stop(self):
		self._alive=False
			
class JSON_Dict(dict):
	def toJSON(self):
		return simplejson.dumps(self)
	def toDict(self):
		return dict(self)
	
def postImport():
	"""get a list of known strories"""
	listStories_Global()
	
def listStories_Global():
	stories_path=os.path.join(PYWEBGAME_PATHS['stories'],'global')
	for cDir in os.listdir(stories_path):
		story_path=os.path.join(stories_path,cDir)
		if (os.path.isdir(story_path)):
			try:
				story_id=md5.new(os.path.join('global',cDir)).hexdigest()
				STORY_INFO[story_id]=JSON_Dict(yaml.load(file(os.path.join(story_path,'story.yaml'),'r')))
				STORY_PATHS[story_id]=story_path
			except yaml.YAMLError, exc:
				cherrypy.log("Unable to parse story.yaml for %s:"%cFile+"\n"+exc)
	return STORY_INFO
	
def listStories_User(user_id=None):
	return {}
	
	
def listStories(user_id=None):
	ret=listStories_Global()
	ret.update(listStories_User(user_id))
	return ret

def getStoryData(user_id,story_id):
	ret=None
	STORY_DATA_LOCK.acquire()
	try:
		s_instance_key=cherrypy.user.id+'.'+story_id
		if (s_instance_key in STORY_INSTANCES):
			ret=STORY_INSTANCES[s_instance_key].Data
	finally:
		STORY_DATA_LOCK.release()
		
	return ret


def readDefaultStoryData(user_id,story_id):
	story_path=STORY_PATHS[story_id]
	try:
		story_data=yaml.load(file(os.path.join(story_path,'defaults.yaml'),'r'))
		story_data['is_new']=True
		STORY_DATA_LOCK.acquire()
		try:
			if not user_id in DEFAULT_STORY_DATA:
				DEFAULT_STORY_DATA[user_id]={}
			
			DEFAULT_STORY_DATA[user_id][story_id]=story_data
		finally:
			STORY_DATA_LOCK.release()
			
	
	except yaml.YAMLError, exc:
		cherrypy.log("Unable to parse story.yaml for %s:"%cFile+"\n"+exc)
		
	return STORY_DATA

		
def newStoryInstance(user_id,story_id):
	readDefaultStoryData(cherrypy.user.id,story_id)
	s_instance_key=cherrypy.user.id+'.'+story_id
	#TODO: check for custom py files
	STORY_INSTANCES[s_instance_key]= app.base_story.Story(
		story_id,
		DEFAULT_STORY_DATA[user_id][story_id],
		DEFAULT_STORY_DATA[user_id][story_id],
		STORY_PATHS[story_id]
	)
	return STORY_INSTANCES[s_instance_key]

def saveStory(user_id,story_id,name,force_path=None):
	rec=re.compile('^[0-9a-zA-Z_\-]+$')
	if not rec.match(name):
		return "Invalid save name!"
	try:
		user_save_path=os.path.join(PYWEBGAME_PATHS['story_saves'],user_id)
		if not os.path.isdir(user_save_path):
			cherrypy.log('Creating save-path for user %s '%(user_id))
			os.mkdir(user_save_path)
		if force_path:
			save_path=os.path.join(user_save_path,force_path)
		else:
			save_path=os.path.join(user_save_path,story_id)
		if not os.path.isdir(save_path):
			cherrypy.log('Creating save-path for user %s / story %s'%(user_id,story_id))
			os.mkdir(save_path)
			
		s_instance_key=cherrypy.user.id+'.'+story_id
		if s_instance_key in STORY_INSTANCES:
			info_file=file(os.path.join(save_path,name+'.info.yaml'), 'w')
			data_file=file(os.path.join(save_path,name+'.data.yaml'), 'w')
			data_file.write(
				yaml.safe_dump(
					STORY_INSTANCES[s_instance_key].dumpData(),
					width=50,
					indent=4
				)
			)
			info_file.write(
				yaml.safe_dump(
					{
						'name':name,
						'story_id':story_id,
						'user_id':user_id,
						'time':time.time(),
						'story_info':STORY_INFO[story_id].toDict(),
					},
					width=50,
					indent=4
				)
			)
			data_file.close()
		else:
			return "Story not running!"
		
	except Exception as e:
		cherrypy.log("Unable to write users save: %s"%str(e))
		return str(e)
	return True

def loadStory(user_id,story_id,name):
	rec=re.compile('^[0-9a-zA-Z_\-]+$')
	if not rec.match(name):
		return "Invalid save name!"
	try:
		user_save_path=os.path.join(PYWEBGAME_PATHS['story_saves'],user_id)
		data_file=file(os.path.join(user_save_path,story_id,name+'.data.yaml'), 'r')
		file_data=yaml.load(data_file)
		s_instance_key=cherrypy.user.id+'.'+story_id
		if not s_instance_key in STORY_INSTANCES:
			newStoryInstance(user_id,story_id)

		STORY_INSTANCES[s_instance_key].loadData(file_data)
	except Exception as e:
		cherrypy.log("Unable to read users save: %s"%str(e))
		return str(e)
	return True
