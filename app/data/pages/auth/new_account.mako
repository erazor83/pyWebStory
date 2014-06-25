<div class="lg_auth_form lg_auth_new_account">
<span style="color:#ff0000;" class="lg_auth_error">${error}</span>
<form method="POST" action="new_account">
  <h1>New User Registration</h1>
  <input type="hidden" name="redirect" value="${redirect}" />
  <input type="hidden" name="openid" value="${openid}" />
  <table>
    ${registration_forms}
    <tr>
      <td>Username${unameEmail}</td>
      <td><input type="text" name="username" value="${username}" /></td>
    </tr>
    ${password_form}
    % if captcha:
      <tr><td colspan="2">${captcha}</td></tr>
    % endif
    <tr>
      <td><input type="submit" value="Submit" /></td>
    </tr>
  </table>
</form>
</div>
