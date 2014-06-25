
var StoryIcons=new Array();
var StoryLists=new Array();

$( document ).ready(function() {
	var StoriesLastObj=new StoryListReader(
		'#last_story',
		'continue',
		"rpc/me?uri=last_story&do=get"
 	);
	StoriesLastObj.read();

	var StoriesNewObj=new StoryListReader(
		'#story_list',
		'new',
		"rpc/me?uri=valid_stories&do=get"
 	);
	StoriesNewObj.read();

	var StoriesSavedObj=new StoryListReader(
		'#story_saves',
		'load_story',
		"rpc/me?uri=last_saved_stories&do=get"
 	);
	StoriesSavedObj.read();

	StoriesSavedObj.OnReady=function(data) {
		this.data=data;
			
		if (this.data) {
			for (var cKey in this.data) {
				this.Icons[cKey]=new StorySaveIcon(
					$().uniqueId(),
					cKey,
					this.data[cKey],
					this.action
				);
			}
		}
		this.display();
	};
	
});


function StoryListReader(target,action,url) {
	this.target=target;
	
	this.url=url;
	
	this.html='';
	this.data='';
	
	this.action=action;
	
	this.Icons=new Array();
	this.IconList=new StoryIconList($().uniqueId(),this.Icons);
	
	this.render=function(story_list_data) {
		return this.IconList.render();
	}
	
	this.read=function(url) {
		var obj=this;
		if (url) {
			this.url=url;
		}
		$.getJSON(this.url, function( data ) {
			obj.OnReady(data);
		});
	}
	this.OnReady=function(data) {
		this.data=data;
		
		if (this.data) {
			for (var cKey in this.data) {
				this.Icons[cKey]=new StoryIcon(
					$().uniqueId(),
					cKey,
					this.data[cKey],
					this.action
				);
			}
		}
		this.display();
	};
	
	this.display=function() {
		this.html=this.render(this.data);
		$(this.target).html(this.html);
	}
}
