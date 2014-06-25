
var save_popup_config = {
	layout: {
		name: 'save_popup_config_layout',
		padding: 4,
		panels: [
			{ type: 'left', size: '50%', resizable: true, minSize: 300 },
			{ type: 'main', minSize: 300 }
		]
	},
	grid: { 
		name: 'save_popup_config_grid',
		columns: [
			{ field: 'name', caption: 'Name', size: '33%', sortable: true, searchable: true },
			{ field: 'time', caption: 'Time', size: '150px', sortable: true },
		],
		multiSelect: false,
		records: [],
		onClick: function(event) {
			var grid = this;
			var form = w2ui.save_popup_config_form;
			event.onComplete = function () {
				var sel = grid.getSelection();
				if (sel.length == 1) {
					//form.recid  = sel[0];
					form.record = $.extend(true, {}, grid.get(sel[0]));
					
					form.refresh();
				} else {
					form.clear();
				}
			}
		}
	},
	form: { 
		name: 'save_popup_config_form',
		fields: [
			{ name: 'name', type: 'text', required: true, html: { caption: 'Name', attr: 'size="40" maxlength="40"' } },
		],
		actions: {
			Cancel: function () {
				w2ui[save_popup_config.grid.name].OnClose=function() {};
				w2popup.close();
			},
			Save: function () {
				var errors = this.validate();
				var save_name=this.record.name;
				if (errors.length > 0) return;
				w2popup.close();
				
				w2ui[save_popup_config.grid.name].OnClose=function() {
					var recs = w2ui[save_popup_config.grid.name].find({ name: save_name});
					if (recs.length) {
						ask_SaveStory_override(StoryID,save_name);
					} else {
						do_SaveStory(StoryID,save_name);
					}
				}
			}
		}
	}
}
$(function () {
	$().w2layout(save_popup_config.layout);
	$().w2grid(save_popup_config.grid);
	$().w2form(save_popup_config.form);
});

function show_SaveStory() {
	w2popup.open({
		title 	: 'Save Story',
		width	: 900,
		height	: 600,
		showMax : true,
		body 	: '<div id="main" style="position: absolute; left: 5px; top: 5px; right: 5px; bottom: 5px;"></div>',
		onOpen  : function (event) {
			event.onComplete = function () {
				window.setTimeout(
					function(){fillGridFromSaves(save_popup_config.grid.name)},
					100
				);
				$('#w2ui-popup #main').w2render('save_popup_config_layout');
				w2ui.save_popup_config_layout.content('left', w2ui.save_popup_config_grid);
				w2ui.save_popup_config_layout.content('main', w2ui.save_popup_config_form);
			};
		},
		onMax : function (event) { 
			event.onComplete = function () {
				w2ui.save_popup_config_layout.resize();
			}
		},
		onMin : function (event) {
			event.onComplete = function () {
				w2ui.save_popup_config_layout.resize();
			}
		},
		onClose : function (event) {
			event.onComplete = function () {
				if (w2ui[save_popup_config.grid.name].OnClose) {
					w2ui[save_popup_config.grid.name].OnClose(event);
				}
			}
		}
	});
}
