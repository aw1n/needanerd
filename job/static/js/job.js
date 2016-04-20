$(document).ready(function() {
	
	var searchMinDate = "+1d";
	var searchMaxDate = "+10y";
	
	$("#startdate").datepicker({
		
		showOn: 'both', 
    	buttonImage: '/static/images/calendar.gif',
    	dateFormat: "mm/yy",
    	changeMonth: true,
	    changeYear: true,
	    showButtonPanel: true,
	    showAnim: "",
	    minDate: searchMinDate,
	    maxDate: searchMaxDate,
	    showButtonPanel: true,
	    
	    beforeShow: function (input, inst) {
	    	
	    	//Weird Datepicker Quirk. You have to use a timeout before setting the focus or you get a recursion error. You also can't use this because
	    	//for some reason this is not set to the correct object after the first selection	    	
	    	setTimeout(function(){$("#startdate").focus();},50);
        	
        	//In some cases the opacity is still set to 0.3 so lets ensure that the calendar looks correct
	    	$("#ui-datepicker-div").css({opacity: 1});
	    	
	    },
	    onClose: function (input, inst) {
	            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
	            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
	            $("#startdate").datepicker('option', 'defaultDate', new Date(year, month, 1));
	            $("#startdate").datepicker('setDate', new Date(year, month, 1));
	            $("#enddate").val("");
	    },
    });
	
	$("#startdate").focus(function () {
		$("#ui-datepicker-div").position({
			my: "center top",
			at: "center bottom",
			of: $(this)
		});
	});
	
	$("#enddate").datepicker({
	    showOn: 'both', 
    	buttonImage: '/static/images/calendar.gif',
    	changeMonth: true,
	    changeYear: true,
	    dateFormat: "mm/yy",
	    showButtonPanel: true,
	    showAnim: "",
	    minDate: searchMinDate,
	    maxDate: searchMaxDate,
	    showButtonPanel: true,
	    beforeShow: function (input, inst) {
	    	
	    	//Weird Datepicker Quirk. You have to use a timeout before setting the focus or you get a recursion error. You also can't use this because
	    	//for some reason this is not set to the correct object after the first selection	    	
	    	setTimeout(function(){$("#enddate").focus();},50);
        	
        	//In some cases the opacity is still set to 0.3 so lets ensure that the calendar looks correct
	    	$("#ui-datepicker-div").css({opacity: 1});
	    	
	    	if ((datestr = $("#startdate").val()).length > 0) {
		    	var year = datestr.substring(datestr.length - 4, datestr.length);
		        var month = datestr.substring(0, 2);
		        $("#enddate").datepicker('option', 'minDate', new Date(year, month, 1));
	    	}
	    	
	    },
	    onClose: function (input, inst) {
	            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
	            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
	            $("#enddate").datepicker('option', 'defaultDate', new Date(year, month, 1));
	            $("#enddate").datepicker('setDate', new Date(year, month, 1));
	            $("#permposition").attr('checked', false);
	    },
    });
    
	$("#enddate").focus(function () {
		$("#ui-datepicker-div").position({
			my: "center top",
			at: "center bottom",
			of: $(this)
		});
	});
	
    //Remove previous datepicker styling
	$("#dpcalcss").remove();
	$("#dpcurrprevnext").remove();
	$("#dpbutton").remove();
	
	//Add new styling
    $('<style id="dpcalcss" type="text/css"> .ui-datepicker-calendar { display: none !important; } </style>').appendTo("head");
	$('<style id="dpcurrprevnext" type="text/css"> .ui-datepicker-current, .ui-datepicker-next, .ui-datepicker-prev { display: none; } </style>').appendTo("head");
	$('<style id="dpbutton" type="text/css"> .ui-datepicker-buttonpane button { float: left; } </style>').appendTo("head");

	$("#permposition").click(function (){
		
		if($(this).prop('checked')){
			$( "#enddate" ).attr('disabled', true);
			$( "#enddate" ).datepicker( "option", "disabled", true );
	    	$( "#enddate" ).val("");
	    	$( "#enddate" ).animate({
				"opacity": 0.5
			},200);
		}else{
			$( "#enddate" ).attr('disabled', false);
			$( "#enddate" ).datepicker( "option", "disabled", false );
	    	$( "#enddate" ).animate({
				"opacity": 1
			},200);
		}

	});

});



function changebtn(){
	if ( asyncRequest.readyState == 4 && asyncRequest.status == 200 ){
	/*
		appbtn = $("#jobid_"+asyncRequest.jobid+"");
		appbtn.html("Applied");
		appbtn.switchClass("btn-primary", "btn-success");
		appbtn.prop("disabled",true);
	*/
	}			
}

function applyJob(objective, jobid, studentid){
	
	try{
	
		if(objective == ""){
			bootbox.alert("You cannot apply to a job until you have addded an objective to your profile");
			return;
		}
		
		appbtn = $("#jobid_"+jobid+"");
		appbtn.html("Applied");
		appbtn.switchClass("btn-primary", "btn-success");
		appbtn.prop("disabled",true);
		
		asyncRequest = new XMLHttpRequest();
		asyncRequest.jobid = jobid;
		asyncRequest.onreadystatechange = changebtn;
		asyncRequest.open( 'GET', "/students/apply/"+studentid+"/"+jobid+"/", true );
		asyncRequest.send( null );
	
	}catch ( exception ){
		bootbox.alert( 'AJAX Request failed.',function() {});
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
			
 			buttoncell=row.insertCell(0);
 			namecell=row.insertCell(1);
			employercell=row.insertCell(2);
			salarycell=row.insertCell(3);
			applycell=row.insertCell(4);
			postingcell=row.insertCell(5);
			
			buttoncell.innerHTML="<button class=\"btn btn-primary\" onclick=\"window.location='/jobs/"+jobs[i].fields.jobpk+"/' \">Show Details</button>";
			namecell.innerHTML=jobs[i].fields.name;
			employercell.innerHTML="<a href='/employers/"+jobs[i].fields.employerpk+"/'>"+jobs[i].fields.employer+"</a>";
			salarycell.innerHTML=jobs[i].fields.salary;
			if(jobs[i].fields.applied==true){
    			applycell.innerHTML="<button id=jobid_"+jobs[i].fields.jobpk+" class=\"btn btn-success\" disabled=True>Applied</button>";
			}else{
    			applycell.innerHTML="<button id=jobid_"+jobs[i].fields.jobpk+" class=\"btn btn-primary\" onClick=\"applyJob(jobid="+jobs[i].fields.jobpk+", studentid="+jobs[i].fields.studentpk+")>Apply</button>";
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
		bootbox.alert( 'AJAX Request failed.', function() {});
	}
}

function removeJobFromEmployerTable(){
	
	row=document.getElementById('row_'+asyncRequest.jobpk)
	row.parentNode.removeChild(row)
}

function deleteJob(jobpk){

	bootbox.confirm("Are you sure you want to delete this job?", function(result) {
		
		if (result==true){
			try{
				
				asyncRequest = new XMLHttpRequest();
				asyncRequest.jobpk=jobpk
				asyncRequest.onreadystatechange = removeJobFromEmployerTable;
				asyncRequest.open( 'GET', "/jobs/delete/"+jobpk+"/", true );
				asyncRequest.send( null );
			
			}catch ( exception ){
				bootbox.alert( 'AJAX Request failed.', function() {});
			}
		}
	});		
}