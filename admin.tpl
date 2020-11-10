<html><head> <h3>{{title}}</h3>

<table>
<tr>
{{!headings}}
</tr>

%for row in rows:
  <tr>
    %for col in row:
       <td>{{col}}</td>
    %end
  </tr>
%end
</table>
<p>Back button takes you home.</p>
</body></html>
