% if error:
<p style="color:red">${error}</p>
% endif

<form action="login_password${admin_qs}" method="POST">
  <input type="hidden" name="redirect" value="${redirect}" />
  <p>
    Password Login:
    <table>
      <tr><td>Username or Email</td><td><input type="text" name="username" autofocus="autofocus"/></td></tr>
      <tr><td>Password</td><td><input type="password" name="password" /></td></tr>
      <tr><td><input type="submit" value="Submit" /></td></tr>
    </table>
  </p>
</form>

<table>
% if forgot_link:
  <tr><td><a href="${forgot_link}">Forgot your password?</a></td></tr>
% endif

% if registration_link:
  <p class="lg_auth_newaccount">
    <a href="${registration_link}">Don't have an account here?  Create one.</a>
  </p>
% else:
  <p class="lg_auth_newaccount">
    New accounts are not allowed.  Contact administrator if you need access.
  </p>
% endif

</table>
