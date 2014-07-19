% if Rooms['lab_secret_entrance']['hidden']:
	% if myActionCount['room::lab.examine']<2:
		<% Page.Sections=[1,2,3] %>

		% if Page.Section==1:
		You're searching...
		% elif Page.Section==2:
		...and searching.
		% elif Page.Section==3:
		...aaaand searching..
		% endif
	% else:
		<% Page.Sections=[1,2] %>
		% if Page.Section==1:
			<b>Something looks pretty strange in the left corner...</b>
		% elif Page.Section==2:
			You've discovered a trapdoor!
			<% Rooms['lab_secret_entrance']['hidden']=False %>
		% endif
	% endif
% else:
There is probably nothing new in this room.
% endif