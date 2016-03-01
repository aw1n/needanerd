function filterStudentsTable(){
	
	if ( asyncRequest.readyState == 4 && asyncRequest.status == 200 ){
	
		table=document.getElementById( 'studentstable' );
		//Delete all rows except the headers
		for(j=table.rows.length; j>1;j--){
			table.deleteRow(j-1);
		}
		
		results=asyncRequest.responseText;
		students=JSON.parse(results);
		for(i=0;i<students.length;++i){
			
			row=table.insertRow(1)
			row.setAttribute("onmouseover", "this.style.backgroundColor='#ffff66';");
 			row.setAttribute("onmouseout", "this.style.backgroundColor='#d4e3e5';");
 			row.setAttribute("width","100%");
			
			namecell=row.insertCell(0)
			majorcell=row.insertCell(1)
			usernamecell=row.insertCell(2)
			emailcell=row.insertCell(3)
			
			namecell.innerHTML="<a href='/students/"+students[i].pk+"/'>"+students[i].fields.first_name+" "+students[i].fields.last_name+"</a>";
			majorcell.innerHTML=students[i].fields.currentmajor;
			usernamecell.innerHTML=students[i].fields.username;
			emailcell.innerHTML=students[i].fields.email;			
		}
	}			
}

function searchStudents(strval){
	
	try{
		asyncRequest = new XMLHttpRequest();
		asyncRequest.onreadystatechange = filterStudentsTable;
		asyncRequest.open( 'GET', "/students/search?str="+strval, true );
		asyncRequest.send( null );
	
	}catch ( exception ){
		alert( 'AJAX Request failed.' );
	}
}

