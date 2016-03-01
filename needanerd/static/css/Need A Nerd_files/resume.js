function confirmDeleteResume(userpk){

	var r=confirm("Are you sure you want to delete your resume");
	if (r==true){
		window.location.href = "/resumes/delete/"+userpk+"/"
	}	
}

function confirmDeleteDegree(resumepk, degreepk){

	var r=confirm("Are you sure you want to remove this degree from your resume?");
	if (r==true){
		window.location.href = "/resumes/"+resumepk+"/degrees/delete/"+degreepk+"/"
	}	
}

function addCertification(){
	
	table=document.getElementById('certificationstable')
	alert("Hello Certificationss Table")
	//row=table.appendChild('<tr><td>Some Skills</td></tr>')

}

function addSkill(){
	
	table=document.getElementById('skillstable')
	alert("Hello Skills Table")
	//row=table.appendChild('<tr><td>Some Skills</td></tr>')

}

function addEmployer(){
	
	table=document.getElementById('employerstable')
	alert("Hello Employers Table")
	//row=table.appendChild('<tr><td>Some Skills</td></tr>')

}
