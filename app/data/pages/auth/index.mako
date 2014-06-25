<p>You are logged in as ${username}</p>
<p>You are a member of the following groups:</p>

<ul>
% for group in groups:
  <li>${group}</li>
% endfor
</ul>
% if not ext_registration:
<p><a href="change_password">Change Password</a></p>
% endif


% if is_admin:
<p><a href="admin/">Admin Interface</a></p>
% endif
            
            