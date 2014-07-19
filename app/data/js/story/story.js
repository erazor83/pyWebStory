var RoomActionsById={};
var RoomActionData = [
	{
		"id": "room_caption",
		"text": "__room_name__",
		"parentid": "-1",
		"subMenuWidth": '85px',
		"action":""
	}
];
var RoomActionSource ={
	datatype: "json",
	datafields: [
		{ name: 'id' },
		{ name: 'parentid' },
		{ name: 'text' },
		{ name: 'action' },
		{ name: 'subMenuWidth' }
	],
	id: 'id',
	localdata: RoomActionData
};

function initUI(){
	$('#message_panel').html('');
	updateNavPanel({'directions':{},'caption':""});
	if (StoryInfo['image']) {
		showImage(StoryInfo['image']);
	} else {
		showImage('');
	}
}
function showImage(img_file) {
	$("#picture").fadeOut(function() { 
		$(this).load(function() { $(this).fadeIn(); }); 
		$(this).attr("src", "images/"+img_file); 
	}); 
}
function showPlayerImage(img_file) {
	$("#player_picture").fadeOut(function() { 
		$(this).load(function() { $(this).fadeIn(); }); 
		$(this).attr("src", "images/characters/player/"+img_file); 
	}); 
}
function updateNavPanel(data) {
	var directions=[
		'N','S','W','E',
		'NW','NE','SW','SE',
		'Up','Down'
	];
	for (var cDirIDX in directions) {
		var cDir=directions[cDirIDX];
		if (data['directions'] && (cDir in data['directions']) && (data['directions'][cDir])) {
			$('#nav_direction_'+cDir).show();
			//$('#nav_direction_Button_'+cDir).attr('title',cDir)
		} else {
			$('#nav_direction_'+cDir).hide();
		}
	}
	//$('#room_actions').html(renderRoomActions(data['caption'],data['actions']));

	//$('#nav_direction_Caption').html();
	if (data['caption']!='') {
		$('#nav_room_label').show();
		$('#jqxRoomMenu').show();
		//$('#jqxMenu_list').show();
	} else {
		$('#nav_room_label').hide();
		$('#jqxRoomMenu').hide();
		//$('#jqxMenu_list').hide();
	}
	if (data['caption']) {
		RoomActionData[0]["text"]=data['caption'];
		
		var item_0=RoomActionData[0];
		RoomActionData=[
			item_0
		];
		
		for (var aid in data['actions']) {
			var action=data['actions'][aid];
			RoomActionsById["room_action_"+aid]=action;
			RoomActionData[Number(aid)+1]={
				"id": "room_action_"+aid,
				"text": lang['actions'][action],
				"parentid": "room_caption",
				"action":action
			};
		}
		RoomActionSource['localdata']=RoomActionData;
		var dataAdapter = new $.jqx.dataAdapter(RoomActionSource);
		dataAdapter.dataBind();
		var records = dataAdapter.getRecordsHierarchy(
			'id', 'parentid', 'items',
			[{ name: 'text', map: 'label'}]
		);
		$('#jqxRoomMenu').jqxMenu({
			source: records,
			height: 30,
			width: '100px',
			clickToOpen:true,
			animationHideDuration:50,	
			animationShowDuration:50
			
		});
		var firstItem = $($("#jqxRoomMenu ul:first").children()[0]);
		/*var width=firstItem.outerWidth(true);*/
		firstItem.css('width', '95px');
		$("#jqxRoomMenu").jqxMenu('setItemOpenDirection', firstItem.attr('id'), 'right', 'up');
	}
}
function renderNavPanel(){
	var ret=
		"<div class=\"nav_position\" id=\"nav_room_label\" style=\"top: 42%; left:45px;width:110px\">"+
			"<div id=\"jqxRoomMenu\" style=\"width: 110px\">"+
			"</div>"+
		"</div>"+
		"<div id=\"nav_direction_N\" class=\"nav_position\" style=\"top: 10px; left:43%\">"+
			"<button id=\"nav_direction_Button_N\" type=\"button\" onclick=\"movePlayer('N')\">N</button>"+
		"</div>"+
		"<div id=\"nav_direction_S\" class=\"nav_position\" style=\"bottom: 10px; left:43%\">"+
			"<button id=\"nav_direction_Button_S\" type=\"button\" onclick=\"movePlayer('S')\">S</button>"+
		"</div>"+
		"<div id=\"nav_direction_W\" class=\"nav_position\" style=\"top: 40%; left:10px\">"+
			"<button id=\"nav_direction_Button_W\" type=\"button\" onclick=\"movePlayer('W')\">W</button>"+
		"</div>"+
		"<div id=\"nav_direction_E\" class=\"nav_position\" style=\"top: 40%; right:10px\">"+
			"<button id=\"nav_direction_Button_E\" title=\"E\" type=\"button\" onclick=\"movePlayer('E')\">E</button>"+
		"</div>"+
		"<div id=\"nav_direction_NW\"  class=\"nav_position\" style=\"top: 20%; left:30px\">"+
			"<button id=\"nav_direction_Button_NW\" type=\"button\" onclick=\"movePlayer('NW')\">NW</button>"+
		"</div>"+
		"<div id=\"nav_direction_NE\" class=\"nav_position\" style=\"top: 20%; right:30px\">"+
			"<button id=\"nav_direction_Button_NE\" type=\"button\" onclick=\"movePlayer('NE')\">NE</button>"+
		"</div>"+
		"<div id=\"nav_direction_SW\" class=\"nav_position\" style=\"bottom: 20%; left:30px\">"+
			"<button id=\"nav_direction_Button_SW\" type=\"button\" onclick=\"movePlayer('SW')\">SW</button>"+
		"</div>"+
		"<div id=\"nav_direction_SE\" class=\"nav_position\" style=\"bottom: 20%; right:30px\">"+
			"<button id=\"nav_direction_Button_SE\" type=\"button\" onclick=\"movePlayer('SE')\">SE</button>"+
		"</div>"+
		"<div id=\"nav_direction_Up\"  class=\"nav_position\" style=\"top: 0px; left:0px\">"+
			"<button id=\"nav_direction_Button_Up\" type=\"button\" onclick=\"movePlayer('Up')\">Up</button>"+
		"</div>"+
		"<div id=\"nav_direction_Down\"  class=\"nav_position\" style=\"bottom: 0px; left:0px\">"+
			"<button id=\"nav_direction_Button_Down\" type=\"button\" onclick=\"movePlayer('Down')\">Down</button>"+
		"</div>";
	return ret;
}

function renderRightAcc() {
	var ret='';
	ret= 
		'<div id="right_accordion">'+
			'<h3>Character</h3>'+
			'<div>fsdfsdfsd</div>'+
			'<h3>Inventory</h3>'+
			'<div>fsdfds</div>'+
		'</div>';
	return ret;
}

function appendToMessagePanel(txt) {
	var doAutoScroll=false;
	var cScroll=$(w2ui['main_panel'].el('left')).scrollTop();
	var tScroll=($(w2ui['main_panel'].el('left'))[0].scrollHeight-$(w2ui['main_panel'].el('left')).height());

	if (cScroll == tScroll) {
		doAutoScroll=true;
	}
	$('#message_panel').append(txt);
	if (doAutoScroll) {
		$(w2ui['main_panel'].el('left')).animate({
			scrollTop: $(w2ui['main_panel'].el('left'))[0].scrollHeight
		}, 200);
	}
}
/*
function appendToMessagePanel(txt) {
	var doAutoScroll=false;
	var cScroll=$('#message_panel').scrollTop();
	var tScroll=($('#message_panel')[0].scrollHeight-$('#message_panel').height());

	if (cScroll == tScroll) {
		doAutoScroll=true;
	}
	$('#message_panel').append(txt);
	if (doAutoScroll) {
		$('#message_panel').animate({
			scrollTop: $('#message_panel')[0].scrollHeight
		}, 200);
	}
}*/

$(function () {
	var toolbar_style = 'padding: 4px; border: 1px solid silver; background-color: #efefdf; border-radius: 3px';
	
	var pstyle = 'border: 1px solid #F0F0C1; padding: 0px;';
	$('#layout').w2layout({
		name: 'layout',
		panels: [
			{ type: 'top',		size: 36,		 	resizable: false,	style: toolbar_style, content: 'top', overflow: 'hidden' },
			//{ type: 'left',		size: 200,		resizable: true,	style: pstyle, content: 'left' },
			{ type: 'main',																		style: pstyle, content: 'main' },
			//{ type: 'right',	size: 200,		resizable: true,	style: pstyle, content: 'right' },
			{ type: 'bottom',	size: 36,		resizable: false,		style: toolbar_style, content: 'bottom' }
		]
	});
	var pstyle = 'background-color: #dfdfdf; border: 1px solid #dfdfdf; padding: 0px;';
	$().w2layout({
		name: 'main_panel',
		panels: [
			{ type: 'left',		size: '50%',		resizable: true,	style: pstyle, content:'<div id=\"message_panel\">...</div>'
			},
			{ type: 'main',										resizable: true,	style: pstyle, 
				content:
				'<img id=\"picture\" src=\"\" width=\"100%\" height=\"100%\"/>'+
				'<div id=\"message_next_button\" class=\"message_next_button\">'+
					'<button type="button\" title=\"next section\" onclick=\"sendPageNextSection()\">Next</button>'+
				'</div>'
			},
			{ type: 'right',	size: 204,			resizable: true,	style: pstyle, content: 'right' },
			{ type: 'bottom',	size: 150,			resizable: false,	style: toolbar_style, content: 'left_bottom' }
		]
	});
	var pstyle = 'background-color: #dfdfdf; border: 1px solid #dfdfdf; padding: 0px;';
	$().w2layout({
		name: 'bottom_panel',
		panels: [
			{ type: 'left',		size: 200,		 	resizable: false,	style: pstyle, content: 'nav' },
			{ type: 'main',										resizable: false,	style: pstyle, content: ''},
			{ type: 'right',	size: 200,			resizable: true,	style: pstyle, content: '<div id="jqxTree_Characters" style="min-height:100%"></div>' }
		]
	});
	$().w2layout({
		name: 'bottom_panel_2',
		panels: [
			{ type: 'left',		size: 200,		 	resizable: true,	style: pstyle, content:
				"<div id=\"jqxTree_Room\" style=\"min-height:100%\">"+
					"<div id=\"jqxMenu_Room\">"+
						"<ul>"+
							"<li>Add Item</li>"+
							"<li>Remove Item</li>"+
							"</ul>"+
					"</div>"+
				"</div>"
			},
			{ type: 'main',		size: "200px",		resizable: false,	style: pstyle, content:
				"<table class=\"player_picture\">"+
					"<tr>"+
						"<td style=\"width:150px\">"+
							"<img id=\"player_picture\" src=\"/images/unknown_player.png\" width=\"100%\" height=\"132px\"/>"+
						"</td>"+
						"<td/>"+
					"</tr>"+
				"</table>"
			},
			{ type: 'right',				resizable: false,	style: pstyle, content: '???' }
		]
	});
	$().w2toolbar({
		name: 'bottom_toolbar',
		items: [
			{ type: 'html',  id: 'item1', html: 'Time'},
			{ type: 'break',  id: 'break0' },
			{ type: 'spacer' },
			{ type: 'break',  id: 'break0' },
			{ type: 'html',  id: 'item1', html: user_name},
			{ type: 'spacer' },
		]
	});
	
	$().w2toolbar({
		name: 'top_toolbar',
		items: [
			{ type: 'menu',   id: 'menu', caption: StoryInfo['name'], overflow: 'hidden', icon: "fa fa-bars fa-fw", items: [
				{ text: 'New', icon: 'fa fa-repeat fa-fw' }, 
				{ text: 'Save', icon: 'fa fa-save fa-fw' }, 
				{ text: 'Load', icon: 'fa fa-paste fa-fw' },
				{ text: 'Exit', icon: 'fa fa-ban fa-fw' },
			]},
			{ type: 'break',  id: 'break0' },
			{ type: 'html',  id: 'story_version', html: StoryInfo['version']},
			{ type: 'spacer' },
			{ type: 'break',  id: 'break0' },
			{ id: 'bt_ql', type: 'button', caption: 'Quick-Load', img: 'fa fa-paste fa-fw' },
			{ id: 'bt_qs', type: 'button', caption: 'Quick-Save', icon: 'fa fa-save fa-fw' },
			{ type: 'spacer' },
			{ type: 'break',  id: 'break0' },
			{ id: 'bt_about', type: 'button', caption: 'About', icon: 'fa fa-question-circle fa-fw' },
		],
		onClick: function (target, info) {
			if ((info.item.id == 'menu') &&  info.subItem) {
				if (info.subItem.id=='New') ask_NewStory(StoryID);
				if (info.subItem.id=='Save') show_SaveStory(StoryID);
				if (info.subItem.id=='Load') show_LoadStory(StoryID);
				if (info.subItem.id=='Exit') ask_ExitStory(StoryID);
			}
			if (info.item.id == 'bt_ql') ask_quickLoad(StoryID);
			if (info.item.id == 'bt_qs') do_quickSave(StoryID);
			if (info.item.id == 'bt_about') show_About();
		}
	});
	


	var pstyle = 'background-color: #dfdfdf; border: 1px solid #dfdfdf; padding: 0px;';
	$().w2layout({
		name: 'right_panel',
		panels: [
			{ type: 'top',		size:36,	resizable: false,	style: toolbar_style, content: 'character_button' },
			{ type: 'main',							resizable: false,	style: pstyle, content: 'character_text' },
			{ type: 'bottom',						resizable: false,	style: pstyle, content: 'misc' }
		]
	});
	

	$().w2sidebar({
		name       : 'inventory',
		topHTML    : '<div style="background-color: #eee; padding: 10px 5px; border-bottom: 1px solid silver">Some HTML</div>',
		bottomHTML : '<div style="background-color: #eee; padding: 10px 5px; border-top: 1px solid silver">Some HTML</div>',
		nodes : [ 
			{ id: 'level-1', text: 'Level 1', img: 'icon-folder', expanded: true, group: true,
			  nodes: [ { id: 'level-1-1', text: 'Level 1.1', icon: 'fa-home' },
					   { id: 'level-1-2', text: 'Level 1.2', icon: 'fa-coffee' },
					   { id: 'level-1-3', text: 'Level 1.3', icon: 'fa-comment-alt' }
					 ]
			},
			{ id: 'level-2', text: 'Level 2', img: 'icon-folder', group: true,
			  nodes: [ { id: 'level-2-1', text: 'Level 2.1', icon: 'fa-star-empty' },
					   { id: 'level-2-2', text: 'Level 2.2', icon: 'fa-star-empty' },
					   { id: 'level-2-3', text: 'Level 2.3', icon: 'fa-star-empty' }
					 ]
			},
			{ id: 'level-3', text: 'Level 3', img: 'icon-folder', group: true,
			  nodes: [ { id: 'level-3-1', text: 'Level 3.1', icon: 'fa-star-empty' },
					   { id: 'level-3-2', text: 'Level 3.2', icon: 'fa-star-empty' },
					   { id: 'level-3-3', text: 'Level 3.3', icon: 'fa-star-empty' }
					 ]
			}
		]
	});
	
	w2ui['layout'].content('bottom', w2ui['bottom_toolbar']);
	w2ui['layout'].content('top', w2ui['top_toolbar']);
	
	w2ui['layout'].content('main', w2ui['main_panel']);
	//w2ui['main_panel'].content('main', w2ui['main_tabs']+"<div id=\"main_tabs_content\">...</div>");
	w2ui['main_panel'].content('bottom', w2ui['bottom_panel']);
	w2ui['main_panel'].content('right', renderRightAcc());
	$("#right_accordion").accordion({animate: false });
	//$("#main_tabs_content").html("<div id=\"message_panel\">...</div>");
	
	w2ui['bottom_panel'].content(
		'left', 
		renderNavPanel()
	);
	w2ui['bottom_panel'].content(
		'main', 
		w2ui['bottom_panel_2']
	);
	
});

$( document ).tooltip();

$( document ).ready(function () {
	//$('#message_next_button').hide();
	//updateNavPanel({'directions':{},'caption':""});

	initUI();
	$.getJSON(
		rpc_path+'me?uri=dump_worldState&story='+StoryID,
		function( data ) {
			w2ui['main_panel'].content('right', _dumpType(data));
		}
	);

	initWebSocket();

	$("#jqxRoomMenu").on('itemclick', function (event) {
		if (RoomActionsById[event.args.id]) {
			sendRoomAction(RoomActionsById[event.args.id]);
		}
			//$("#eventLog").text("Id: " + event.args.id + ", Text: " + $(event.args).text());
	});

	var contextMenu = $("#jqxMenu_Room").jqxMenu({ width: '120px',  height: '56px', autoOpenPopup: false, mode: 'popup' });
	var clickedItem = null;
	var source_Room = [
		{ label: "Item 1", expanded: true, items: [
				{ label: "Item 1.1" },
				{ label: "Item 1.2", selected: true }
			]
		},
		{ label: "Item 2" },
				{ label: "Item 3" },
				{ label: "Item 4", items: [
					{ label: "Item 4.1" },
					{ label: "Item 4.2" }
				]
				},
				{ label: "Item 5" },
				{ label: "Item 6" },
				{ label: "Item 7" }
	];
	var attachContextMenu = function () {
		// open the context menu when the user presses the mouse right button.
		$("#jqxTree_Room li").on('mousedown', function (event) {
			var target = $(event.target).parents('li:first')[0];
			var rightClick = isRightClick(event);
			if (rightClick && target != null) {
				$("#jqxTree_Room").jqxTree('selectItem', target);
				var scrollTop = $(window).scrollTop();
				var scrollLeft = $(window).scrollLeft();
				contextMenu.jqxMenu('open', parseInt(event.clientX) + 5 + scrollLeft, parseInt(event.clientY) + 5 + scrollTop);
				return false;
			}
		});
	}
	$(document).on('contextmenu', function (e) {
		if ($(e.target).parents('.jqx-tree').length > 0) {
			return false;
		}
		return true;
	});
	function isRightClick(event) {
		var rightclick;
		if (!event) var event = window.event;
		if (event.which) rightclick = (event.which == 3);
		else if (event.button) rightclick = (event.button == 2);
			return rightclick;
	}
	$('#jqxTree_Room').jqxTree({ source: source_Room});
	attachContextMenu();

	var source_Characters = [
		{ label: "Kim"},
		{ label: "Tom" }
	];
	$('#jqxTree_Characters').jqxTree({ source: source_Characters});

});
