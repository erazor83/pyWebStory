So, you're standing before a front-door. Now what?
<br/>
% if visits<3:
You look around... everything seems pretty new to you.

% elif visits<10:
This room starts to bore you.

% else:
You've been here ${visits} times.

% endif