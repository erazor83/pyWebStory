var currentPortal = null;

function initWebSocket() {
	currentPortal=portal.open(ws_path+StoryID).on({
			// Pseudo event
			connecting: function(data) {
				appendToMessagePanel("connecting<br/>");
			}, // The selected transport starts connecting to the server
			
			waiting: function(delay, attempts) {}, // The socket waits out the reconnection delay
			
			// Network event
			open: function() {
				appendToMessagePanel("open<br/>");
				currentPortal.send("greeting", "Hi"); // Send an event whose name is 'greeting' and data is 'Hi' to the server
			}, // The connection is established successfully and communication is possible
			
			close: function(reason) {
				appendToMessagePanel("close<br/>"+reason);
			}, // The connection has been closed or could not be opened
			
			// Message event
			message: function(data) {
				//appendToMessagePanel(data[0]+"<br/>") ;
				if (data[0]=='err') {
					if (data[1]=='invalid_session') {
						gotoIndexPage();
					}
				} else if (data[0]=='room::info') {
					updateNavPanel(data[1]);
					if (data[1]['image']) {
						showImage('rooms/'+data[1]['image']);
					}
				} else if (data[0]=='character::info') {
					if (data[1]['type']=='player') {
						if (data[1]['image']) {
							showPlayerImage('character/player/'+data[1]['image']);
						}
					}
				} else if (data[0]=='page::done'){
					if (data[1]) {
						//no more sections
						$('#message_next_button').hide();
					} else{
						//we have more sections
						$('#message_next_button').show();
					}
				} else if (data[0]=='text'){
					appendToMessagePanel(data[1]+"<br/>") ;
				}
			}, // Receive an event whose name is message sent by the server
			
			event: function(data) {
				//appendToMessagePanel("event<br/>"+data);
				if (data=='story::new') {
					initUI();
				} else if (data=='story::exit') {
					gotoIndexPage();
				}
			} // Receive an event whose name is event sent by the server
	});
}

function sendPageNextSection() {
	$('#message_next_button').hide();
	sendAction('Page.nextSection',false);
}
function sendAction(name,data) {
	//appendToMessagePanel("Action: "+name);
	currentPortal.send("message", ['action',name,data]);
}

function movePlayer(direction) {
	sendAction('Player.moveToDirection',direction);
}
function sendRoomAction(action) {
	//$("#jqxRoomMenu").jqxMenu('close');
	$("#jqxRoomMenu").jqxMenu('closeItem', 'room_caption');
	sendAction('Room.action',action);
}