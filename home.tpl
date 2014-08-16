<h1>Site Admin Panel</h1>
<h4>Select a Phone for Opinion Summarization</h4>
<form action='/second' method='post'>
	<select name='phone'>
	%for r in row:
		<option value="{{r[1]}}">{{r[1]}}</option>
	%end
	</select>
	
	<input type='submit'/>
</form>
<div>
<form action='/third' method='post'>
	<h4>Add a Phone for Review</h4>
	<br>
	<Enter Phone Name or URL>
	<input type='text' name='pname'/>
	<input type='submit' value="Submit Phone">
</form>
</div>
