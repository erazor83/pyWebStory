<% Page.Sections=[1,2] %>
% if Page.Section==1:
	<h1>Welcome!</h1>
	<br/>
	So you just started a new story and read this page, huh?<br/>
	<br/>
	Great! So this is HTML and it comes from new.mako.<br/>
	<br/>
	You can even add images in here:<br/>
	<img src="images/example.jpg"/>
	<br/>
	Have some <b>fun</b>!<br/>
% elif Page.Section==2:
<% me.moveToRoom('front_door') %>

% endif
