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
			
			studentpk=students[i].fields.studentid;
			row=table.insertRow(1);
			
			namecell=row.insertCell(0);
			majorcell=row.insertCell(1);
			objectivecell=row.insertCell(2);
			contactcell=row.insertCell(3);
			
			namecell.innerHTML="<a href='/students/"+studentpk+"/'>"+students[i].fields.first_name+" "+students[i].fields.last_name+"</a>";
			majorcell.innerHTML=students[i].fields.currentmajor;
			objectivecell.innerHTML=students[i].fields.objective;
			contactcell.innerHTML="<td><button class='btn btn-primary' onclick=window.location='/contact/"+studentpk+"/' >Contact</button></td>"
			
		}
		
		$("#top10").html("*Top 10 search results shown");
		$("#pagination").html("");
		
	}			
}

function searchStudents(strval){
	
	try{
		if(strval != ""){
			asyncRequest = new XMLHttpRequest();
			asyncRequest.onreadystatechange = filterStudentsTable;
			asyncRequest.open( 'GET', "/students/search?str="+strval, true );
			asyncRequest.send( null );
		}	
	
	}catch ( exception ){
		bootstrap.alert( 'AJAX Request failed.', function() {});
	}
}

