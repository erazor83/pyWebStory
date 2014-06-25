% if error:
<p style="color:red">${error}</p>
% endif

<form action="change_password" method="POST">
<input type="hidden" name="redirect" value="${redirect}">
<table>
	<tr>
		<td>Change Password: </td>
		<td><input type="password" name="newpass"/></td>
	</tr>
	<tr>
		<td>New Password (again)</td>
		<td><input type="password" name="newpass2"/></td>
	</tr>
	<tr>
		<td/>
		<td><input type="submit" value="Submit"/></td>
	</tr>
</table>
</form> 
