
//input type="button" value="Show Alert" onclick="w2alert('message')">

function ask_LoadSave(story_id,save_name) {
	w2confirm(
		'Do you really want to load the save "'+save_name+'"?<br/>Current story will <b>not</b> be saved!', 
		function (btn) {
			//console.log(btn);
			//console.log(story_id);
			if (btn=='Yes') {
				do_LoadSave(story_id,save_name);
			}
		}
	);
}
function do_LoadSave(story_id,save_name) {
	$.getJSON(
			rpc_path+'me?do=load_story&story='+story_id+'&name='+save_name,
			function( data ) {
				if (data==true) {
					w2alert('Game loaded.');
					appendToMessagePanel('Load done.<br/>');
				} else if (data!=false) {
					w2alert('Game not loaded. <br/>'+data);
					appendToMessagePanel('Load failed.<br/>');
				} else {
					w2alert('Game not loaded.');
					appendToMessagePanel('Load failed.<br/>');
				}
			}
		);
}

function ask_quickLoad(story_id) {
	w2confirm(
		'Do you really want to load the quicksave?<br/>Current story will <b>not</b> be saved!', 
		function (btn) {
			//console.log(btn);
			//console.log(story_id);
			if (btn=='Yes') {
				do_quickLoad(story_id);
			}
		}
	);
}

function do_quickLoad(story_id) {
	$.getJSON(
			rpc_path+'me?do=quickload_story&story='+story_id,
			function( data ) {
				if (data==true) {
					w2alert('Game loaded.');
					appendToMessagePanel('Quickload done.<br/>');
				} else if (data!=false) {
					w2alert('Game not loaded. <br/>'+data);
					appendToMessagePanel('Quickload failed.<br/>');
				} else {
					w2alert('Game not loaded.');
					appendToMessagePanel('Quickload failed.<br/>');
				}
			}
		);
}

function do_quickSave(story_id) {
	$.getJSON(
			rpc_path+'me?do=quicksave_story&story='+story_id,
			function( data ) {
				if (data==true) {
					w2alert('Game saved.');
					appendToMessagePanel('Quicksave done.<br/>');
				} else if (data!=false) {
					w2alert('Game not saved. <br/>'+data);
					appendToMessagePanel('Quicksave failed.<br/>');
				} else {
					w2alert('Game not saved.');
					appendToMessagePanel('Quicksave failed.<br/>');
				}
			}
		);
}

function ask_SaveStory_override(story_id,name) {
	w2confirm(
		'Do you really want to <b>override</b> the save "'+name+'"?', 
		function (btn) {
			if (btn=='Yes') {
				do_SaveStory(story_id,name);
			}
		}
	);
}
function do_SaveStory(story_id,name) {
	if (name=='Quicksave') {
		name='__quicksave__';
	}
	$.getJSON(
			rpc_path+'me?do=save_story&story='+story_id+'&name='+name,
			function( data ) {
				if (data==true) {
					w2alert('Game saved.');
					appendToMessagePanel('Save done.<br/>');
				} else if (data!=false) {
					w2alert('Game not saved. <br/>'+data);
					appendToMessagePanel('Save failed.<br/>');
				} else {
					w2alert('Game not saved.');
					appendToMessagePanel('Save failed.<br/>');
				}
			}
		);
}