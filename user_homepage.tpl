<h3>User HomePage</h3>
<form action='/summary_display' method='post'>
	<h3>Select a phone for summarized Reviews</h3>
	<select name='phone'>
	%for r in row:
		<option value="{{r[1]}}">{{r[1]}}</option>
	%end
	</select>
	<input type='submit' Value='View Results'/>
</form>

<form action='/test' method='post'>
	<h3>Write Reviews and Click on submit to View a summarized Version</h3>
	<textarea rows=5 cols=150 name='review'></textarea>
	<input type='submit'/>
</form>
