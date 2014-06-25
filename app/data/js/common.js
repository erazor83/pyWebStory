function StoryIconList(id,icons) {
	this.id=id;
	this.Icons=icons;

	this.render=function() {
		var ret='';
		if (this.Icons) {
			ret='<table>';
			ret=ret+'<tr>';
			for (var cIconKey in this.Icons) {
				var cIcon=this.Icons[cIconKey];
				ret=ret+'<td>';
				ret=ret+cIcon.render();
				ret=ret+'</td>';
			}
			ret=ret+'</tr>';
			ret=ret+'</table>';
			
		} else {
			ret='error';
		}
		return ret;
	}
}

var STORY_DATA_MAP=new Array();
function StorySaveIcon(id,StoryKey,data,action) {
	this.id=id;
	this.data=data;
	this.StoryKey=StoryKey;
	this.action=action;
	STORY_DATA_MAP["last_save:"+this.id]=data;

	this.render=function() {
		if (this.action) {
			var cStoryData=this.data;
			var name=this.data['name'];
			var name_short=name;
			if (name=='__quicksave__') {
				name="<font style=\"color:green\">Quicksave</font>";
				name_short=name;
			} else {
				if (name.length>10) {
					name_short=name.substr(0,10)+'...';
				}
			}
			return "<div class=\"small_story_icon_action\" "+
				"onmouseover=\"showStorySaveOverlay(this,\'"+this.StoryKey+"\',\'last_save:"+this.id+"\')\""+
				"onclick=\"window.location.href='?do="+this.action+"&story="+this.StoryKey+
					"&name="+this.data['name']+"';\">"+
					this.data['story_info']['name']+"<br/>"+
					"<small>"+this.data['story_info']['version']+"</small><br/>"+
					"<small>"+name_short+"</small>"+
					"</div>";
		} else {
			return "<div class=\"small_story_icon\">"+this.StoryKey+"</div>";
		}
	}
}

function StoryIcon(id,StoryKey,data,action) {
	this.id=id;
	this.data=data;
	this.StoryKey=StoryKey;
	this.action=action;
	STORY_DATA_MAP[this.id]=data;

	this.render=function() {
		if (this.action) {
			var cStoryData=this.data;
			return "<div class=\"small_story_icon_action\" onmouseover=\"showStoryOverlay(this,\'"+this.StoryKey+"\',\'"+this.id+"\')\" onclick=\"window.location.href='?do="+this.action+"&story="+this.StoryKey+"';\">"+
					this.data['name']+"<br/>"+
					"<small>"+this.data['version']+"</small>"+
					"</div>";
		} else {
			return "<div class=\"small_story_icon\">"+this.StoryKey+"</div>";
		}
	}
}

function showStoryOverlay(obj, story_id,dom_id) {
	$('#story_overlay_title').html(STORY_DATA_MAP[dom_id]['name']);
	$('#story_overlay_version').html(STORY_DATA_MAP[dom_id]['version']);
	$('#story_overlay_author').html(STORY_DATA_MAP[dom_id]['author']);
	$('#story_overlay_copyright').html(STORY_DATA_MAP[dom_id]['copyright']);
	$('#story_overlay_description').html(STORY_DATA_MAP[dom_id]['description']);
	$(obj).w2overlay($('#story_overlay [rel=body]').html(), { left:40, css: { width: '200px', padding: '2px' } });
}
function showStorySaveOverlay(obj, story_id,dom_id) {
	var name=STORY_DATA_MAP[dom_id]['name'];
	if (name=='__quicksave__') {
		name="<font style=\"color:green\">Quicksave</font>";
	}
	$('#story_save_overlay_title').html(STORY_DATA_MAP[dom_id]['story_info']['name']);
	$('#story_save_overlay_version').html(STORY_DATA_MAP[dom_id]['story_info']['version']);
	$('#story_save_overlay_author').html(STORY_DATA_MAP[dom_id]['story_info']['author']);
	$('#story_save_name').html(name);
	$('#story_save_date').html($.format.prettyDate(STORY_DATA_MAP[dom_id]['time']*1000));
	$(obj).w2overlay($('#story_save_overlay [rel=body]').html(), { left:40, css: { width: '250px', padding: '2px' } });
}

function gotoIndexPage() {
	window.location.href=URL_INDEX_PAGE;
}

// popup based on HTML already on the page
$('#story_overlay').w2popup();

// overlay based on the same HTML
$().w2overlay($('#story_overlay [rel=body]').html(), { css: { width: '200px', padding: '2px' } });

// popup based on HTML already on the page
$('#story_save_overlay').w2popup();

// overlay based on the same HTML
$().w2overlay($('#story_save_overlay [rel=body]').html(), { css: { width: '200px', padding: '2px' } });


function show_About(){
	w2popup.open({
		title   : 'About PyWebStory',
		body    : 
		'An interactive story telling engine using: <br/>'+
		'<ul>'+
			'<li>cheeryPy + lameauthority + websockets</li>'+
			'<li>jQuery</li>'+
			'<li>jQueryUi</li>'+
			'<li>W2UI</li>'+
			'<li>JQWidgets</li>'+
			'<li>Portal</li>'+
			'<li>jQuery-dateFormat</li>'+
		'</ul>'+
		'<br/>'+
		'Thanks to all supporters!</br>'+
		'<div style="bottom:2px;right:2px;position:fixed">&copy; 2014 Alexander \'E-Razor\' Krause</div>'
	});
}