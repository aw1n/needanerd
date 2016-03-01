function changebtn(){
	if ( asyncRequest.readyState == 4 && asyncRequest.status == 200 ){
	
		button=document.getElementById( 'jobid_'+asyncRequest.jobid);
		button.value = "Applied";
		button.disabled=true;
	}			
}

function applyJob(jobid, studentid){
	
	try{
	
		asyncRequest = new XMLHttpRequest();
		asyncRequest.jobid = jobid;
		asyncRequest.onreadystatechange = changebtn;
		asyncRequest.open( 'GET', "/students/apply/"+studentid+"/"+jobid+"/", true );
		asyncRequest.send( null );
	
	}catch ( exception ){
		alert( 'AJAX Request failed.' );
	}
}

function filterJobsTable(){
	
	if ( asyncRequest.readyState == 4 && asyncRequest.status == 200 ){
	
		table=document.getElementById( 'applyjobstable' );
		//Delete all rows except the headers
		for(j=table.rows.length; j>1;j--){
			table.deleteRow(j-1);
		}
		
		results=asyncRequest.responseText;
		jobs=JSON.parse(results);
		for(i=0;i<jobs.length;++i){
			
			row=table.insertRow(1)
			row.setAttribute("onmouseover", "this.style.backgroundColor='#ffff66';");
 			row.setAttribute("onmouseout", "this.style.backgroundColor='#d4e3e5';");
 			row.setAttribute("width","100%");
			
 			buttoncell=row.insertCell(0)
 			namecell=row.insertCell(1)
			employercell=row.insertCell(2)
			salarycell=row.insertCell(3)
			applycell=row.insertCell(4)
			postingcell=row.insertCell(5)
			
			buttoncell.innerHTML="<input type=button value=\"Show Details\" onclick=\"window.location='/jobs/"+jobs[i].fields.jobpk+"/' \"/>"
			namecell.innerHTML=jobs[i].fields.name;
			employercell.innerHTML="<a href='/employers/"+jobs[i].fields.employerpk+"/'>"+jobs[i].fields.employer+"</a>";
			salarycell.innerHTML=jobs[i].fields.salary;
			if(jobs[i].fields.applied==true){
    			applycell.innerHTML="<input id=jobid_"+jobs[i].fields.jobpk+" type=button value=\"Applied\" disabled=True>"
			}else{
    			applycell.innerHTML="<input id=jobid_"+jobs[i].fields.jobpk+" type=button value=\"Apply\" onClick=\"applyJob(jobid="+jobs[i].fields.jobpk+", studentid="+jobs[i].fields.studentpk+")\">"
			}
			postingcell.innerHTML=jobs[i].fields.updated_at;			
		}
	}			
}

function searchJobs(strval){
	
	try{
		asyncRequest = new XMLHttpRequest();
		asyncRequest.onreadystatechange = filterJobsTable;
		asyncRequest.open( 'GET', "/jobs/search?str="+strval, true );
		asyncRequest.send( null );
	
	}catch ( exception ){
		alert( 'AJAX Request failed.' );
	}
}

function removeJobFromEmployerTable(){
	
	row=document.getElementById('row_'+asyncRequest.jobpk)
	row.parentNode.removeChild(row)
}

function deleteJob(jobpk){

	var r=confirm("Are you sure you want to delete this job?");
	if (r==true){
		try{
			
			asyncRequest = new XMLHttpRequest();
			asyncRequest.jobpk=jobpk
			asyncRequest.onreadystatechange = removeJobFromEmployerTable;
			asyncRequest.open( 'GET', "/jobs/delete/"+jobpk+"/", true );
			asyncRequest.send( null );
		
		}catch ( exception ){
			alert( 'AJAX Request failed.' );
		}
	}	
}