
var load_popup_config = {
	layout: {
		name: 'load_popup_config_layout',
		padding: 4,
		panels: [
			{ type: 'main'},
			{ type: 'bottom',size: '40px', minSize: 40}
		]
	},
	grid: { 
		name: 'load_popup_config_grid',
		columns: [
			{ field: 'name', caption: 'Name', size: '33%', sortable: true, searchable: true },
			{ field: 'time', caption: 'Time', size: '150px', sortable: true },
		],
		multiSelect: false,
		records: [],
		onClick: function(event) {
			var grid = this;
			var form = w2ui.load_popup_config_form;
			event.onComplete = function () {
				var sel = grid.getSelection();
				if (sel.length == 1) {
					$('#load_popup_config_layout__loadButton').prop('disabled', false);
					/*
					//form.recid  = sel[0];
					form.record = $.extend(true, {}, grid.get(sel[0]));
					form.refresh();*/
				} else {
					
				}
			}
		},
		onLoad: function(event) {
			var rec_id=this.getSelection();
			var rec=this.get(rec_id[0]);
			var rec_data=rec._data;
			this.OnClose=function(event) {
				ask_LoadSave(rec_data['story_id'],rec['name']);
			};
			w2popup.close();
		}
	}
}
$(function () {
	$().w2layout(load_popup_config.layout);
	$().w2grid(load_popup_config.grid);
});

function show_LoadStory() {
	w2popup.open({
		title 	: 'Load Story',
		width	: 900,
		height	: 600,
		showMax : true,
		body 	: '<div id="main" style="position: absolute; left: 5px; top: 5px; right: 5px; bottom: 5px;"></div>',
		onOpen  : function (event) {
			event.onComplete = function () {
				window.setTimeout(
					function(){fillGridFromSaves(load_popup_config.grid.name)},
					100
				);
				$('#w2ui-popup #main').w2render('load_popup_config_layout');
				w2ui.load_popup_config_layout.content(
					'main',
					w2ui.load_popup_config_grid
				);
				w2ui.load_popup_config_layout.content(
					'bottom',
					"<table style=\"width:100%;text-align:center\">"+
						"<tr>"+
							"<td>"+
								"<input type=\"button\" value=\"Cancel\" onclick=\"w2popup.close();\">"+
							"</td>"+
							"<td>"+
								"<input id=\"load_popup_config_layout__loadButton\" disabled=\"disabled\" "+
									"type=\"button\" value=\"Load\" "+
									"onclick=\"w2ui['load_popup_config_grid'].onLoad()\">"+
							"<td>"+
						"<tr>"+
					"</table>"
				);
		
				//w2ui.load_popup_config_layout.load(base_path+'me/');
			};
		},
		onMax : function (event) { 
			event.onComplete = function () {
				w2ui.load_popup_config_layout.resize();
			}
		},
		onMin : function (event) {
			event.onComplete = function () {
				w2ui.load_popup_config_layout.resize();
			}
		},
		onClose : function (event) {
			event.onComplete = function () {
				if (w2ui[load_popup_config.grid.name].OnClose) {
					w2ui[load_popup_config.grid.name].OnClose(event);
				}
			}
		}
	});
}

function show_LoadError(grid_name) {
	w2ui[grid_name].OnClose=function() {
		w2alert('Unable to get savelist!');
	};
	w2popup.close();

}

function fillGridFromSaves(grid_name) {
	w2popup.lock('Loading...', true);

	$.getJSON(
		rpc_path+'me?do=get&uri=story_saves&story='+StoryID,
		function( data ) {
			if (data) {
				w2ui[grid_name].clear();
				var g = 1;
				for (var cSave in data) {
					var time_str=$.format.date(Math.round(data[cSave]['time']*1000),'dd/MM/yyyy HH:mm:ss');
					if (data[cSave]['name']=='__quicksave__') {
						w2ui[grid_name].add([{
							recid: g,
							name: "Quicksave",
							time: time_str,
							style: "color: green",
							_data:data[cSave]
						}]);
					} else {
						w2ui[grid_name].add([{
							recid: g,
							name: data[cSave]['name'],
							time: time_str,
							_data:data[cSave]
						}]);
					}
					g=g+1;
				}
				w2popup.unlock();
			} else {
				show_LoadError(grid_name);
			}
		}
	)
		.fail(function() {
			show_LoadError(grid_name);
		});
}