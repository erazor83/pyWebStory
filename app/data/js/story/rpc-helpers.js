function ask_ExitStory(story_id) {
	w2confirm(
		'Do you really want to exit this story?<br/>Current story <b>will</b> be saved and you can continue later!', 
		function (btn) {
			if (btn=='Yes') {
				do_exitStory(story_id);
			}
		}
	);
}
function do_exitStory(story_id) {
	$.getJSON(
			rpc_path+'me?do=exit_story&story='+story_id,
			function( data ) {
				if (data==true) {
					gotoIndexPage();
				} else if (data!=false) {
				} else {
				}
			}
		);
}

function ask_NewStory(story_id) {
	w2confirm(
		'Do you really want to restart this story?<br/>Current story will <b>not</b> be saved!', 
		function (btn) {
			if (btn=='Yes') {
				do_newStory(story_id);
			}
			//console.log(btn);
			//console.log(story_id);
		}
	);
}
function do_newStory(story_id){
	//means save story to last_state
	//move to index-page
	$.getJSON(
			rpc_path+'me?do=new_story&story='+story_id,
			function( data ) {
				if (data==true) {
				} else {
				}
			}
		);
}