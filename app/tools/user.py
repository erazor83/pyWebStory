__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2014-03-11"
__version__	= "0.1.0"
__license__ = "Creative Commons Attribution-NonCommercial 3.0 License."

PYWEBGAME_PATHS = None
USER_DATA_LOCK=None
USER_DATA=None
import yaml
import os

def postImport():
	pass

def getLastStory():
	return {}

def listSavedStories(user_id,story_id=None):
	user_save_path=PYWEBGAME_PATHS['story_saves']+user_id+'/'
	if not os.path.isdir(user_save_path):
		cherrypy.log('Creating save-path for user %s '%(user_id))
		os.mkdir(user_save_path)
		return {}
	
	if story_id==None:
		story_list=os.listdir(user_save_path)
	else:
		story_list=[story_id]
		
	saves={}
	for cID in story_list:
		save_path=user_save_path+cID+'/'
		for cName in os.listdir(save_path):
			try:
				if cName.find('.info.yaml')!=-1:
					info_file=file(save_path+cName, 'r')
					info_data=yaml.load(info_file)
					if not cID in saves:
						saves[cID]={}
					saves[cID][cName[0:-10]]=info_data
			except Exception as e:
				print(e)
	return saves

def getStorySaves(user_id,story_id):
	saves=listSavedStories(user_id,story_id)
	if story_id in saves:
		return saves[story_id]
	else:
		return {}