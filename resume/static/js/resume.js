var degree = {

	type:'',
    major:'',
    university:'',
    date:'',
    gpa:'',
    honors:'',

}
    
var cert = {
	name:'',
	authority:'',
	licnumber:'',
	url:'',
	expdate:'',
	neverexp:''
};

var job = {
	company:'',
	title:'',
	jobfunctions:'',
	startdate:'',
	enddate:'',
};

var skill = {
	skill:'',
};

var degreelist = [];
var degreecount = 0
;
var certlist = [];
var certcount = 0;

var empllist = [];
var jobcount = 0

var skilllist = [];
var numskills = 0;

function updateResume(data){
	
	$.ajax({
		url: "/resumes/update/"+ $("#resumepk").val() +"/",
		beforeSend: function(xhr){xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))},
		context: document.body,
		data: data,
		dataType: "json",
		type: "POST",
	}).done(function() {
		//alert("it says it worked");
		//$( this ).addClass( "done" );
		

	}).fail(function() {
		//alert("it says it failed");
		//$( this ).addClass( "done" );
	}).always(function() {
		//$( this ).addClass( "done" );
	});

}

function editEmail(){
	$('#email').removeProp('readonly');
	$('#editemail').html('<span id="editemailspan" class="glyphicon glyphicon-ok"></span> Save');
	$('#editemail').click(function (){
		
		var data = {
				email: $("#email").val(),
		}
		$.ajax({
			url: "/students/update/"+$("#studentpk").val() +"/",
			beforeSend: function(xhr){xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))},
			context: document.body,
			data: data,
			dataType: "json",
			type: "POST",
		}).done(function(data) {
			bootbox.alert( 'Email address successfully updated. Please make sure to validate your new email address',function() {
				$('#email').prop('readonly', true);
				$('#editemail').html('<span id="editemailspan" class="glyphicon glyphicon-ok"></span> Edit');
				$("#editemail").off('click');
				$("#editemail").click(editEmail);
			});
		}).fail(function() {
			bootbox.alert( 'Failed to update the email address, most likely because it is already registered to another user or had an invalid format. Contact need a nerd if you belive this an error.',function() {});
				$('#email').prop('readonly', true);
				$('#editemail').html('<span id="editemailspan" class="glyphicon glyphicon-ok"></span> Edit');
				$("#editemail").off('click');
				$("#editemail").click(editEmail);
		}).always(function() {
			
		});
		
	});
}

function editMajor(){
	$('#major').removeProp('readonly');
	$('#editmajor').html('<span id="editmajorspan" class="glyphicon glyphicon-ok"></span> Save');
	$('#editmajor').click(function (){
		var data = {
			major: $("#major").val(),
		}
		$.ajax({
			url: "/students/update/"+$("#studentpk").val() +"/",
			beforeSend: function(xhr){xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))},
			context: document.body,
			data: data,
			dataType: "json",
			type: "POST",
		}).done(function(data) {
			bootbox.alert( 'Current major successfully updated',function() {
				$('#major').prop('readonly', true);
				$('#editmajor').html('<span id="editmajorspan" class="glyphicon glyphicon-ok"></span> Edit');
				$("#editmajor").off('click');
				$("#editmajor").click(editMajor);
			});
		}).fail(function() {
			bootbox.alert( 'Failed to update, contact need a nerd',function() {});
				$('#major').prop('readonly', true);
				$('#editmajor').html('<span id="editmajorspan" class="glyphicon glyphicon-ok"></span> Edit');
				$("#editmajor").off('click');
				$("#editmajor").click(editMajor);
		}).always(function() {
			
		});
	});
}

function createDegree(data){
	
	$.ajax({
		url: "/resumes/" + $("#resumepk").val() +"/degrees/add/",
		beforeSend: function(xhr){xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))},
		context: document.body,
		data: data,
		dataType: "json",
		type: "POST",
	}).done(function(data) {
		//It worked
		addDegreeHTML(false, data[0].pk);	
	}).fail(function() {
		//alert("it says it failed");
		//$( this ).addClass( "done" );
	}).always(function() {
		//$( this ).addClass( "done" );
	});

}

/*
 * function: addDegreeHTML
 * prereqs: the degree global variable is updated
 */
function addDegreeHTML(readOnly, degreeID){
	
	$('#newdegree').html('');
	saveddegrees = $('#saveddegrees');
	
	toAppend='<div id=\"degree'+degreeID+ '\"\">';
	toAppend+='<h3><strong>' + degree.university+'';
	
	if(!readOnly){
		toAppend+='<button type=\"button\" id=\"remdegreebutton'+degreeID+ '\" class=\"btn-default\" ><span class=\"glyphicon glyphicon-remove-sign\"></span></button>';
	}
	
	toAppend+='<h4>'+degree.degreetype+', '+ degree.major;
	if(degree.honors.length > 0){
		toAppend+=', '+ degree.honors;
	}
	if(degree.gpa.length > 0){
		toAppend+=', '+ degree.gpa;
	}
	toAppend+='</h4>';
	toAppend+='<h4><small>'+ degree.date+'</small></h4></div>';
	
	saveddegrees.append(toAppend);
	
	if(!readOnly){
	
		$("#remdegreebutton"+degreeID).toggleClass('pull-right');
		
		$("#remdegreebutton"+degreeID).hover(function (){
			$(this).toggleClass('btn-danger');
		});
		$("#remdegreebutton"+degreeID).click(function (){
			
			thistext = this.id;
			toRemove = 'remdegreebutton';
			realDegreeID = thistext.replace(toRemove,'');
			
			//necessary because bootbox becomes the new "this"
			thisdegree=this;
			
			bootbox.confirm("Are you sure you want to remove this degree from your resume?", function(result) {

				if (result==true){
					deleteDegree(realDegreeID);
					$(thisdegree).parent().closest('div').remove();
				}
			
			});
			
		});
	}
	
	$( "*" ).animate({"opacity": 1},200);
	$( "*" ).attr('disabled', false);
	
	$("#noeducation").html('');
	degreelist.push(degree);
	degreecount++;

}

function deleteDegree(degreeID){
	
	$.ajax({
		url: "/resumes/" + $("#resumepk").val() +"/degrees/delete/"+degreeID+"/",
		beforeSend: function(xhr){xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))},
		type: "DELETE",
	}).done(function() {
		--degreecount;
		if(degreecount==0){
			$("#noeducation").html(noeducationtext);
		}
		//alert("it says it worked");
		//$( this ).addClass( "done" );
	}).fail(function() {
		//alert("it says it failed");
		//$( this ).addClass( "done" );
	}).always(function() {
		//$( this ).addClass( "done" );
	});

}

function createWorkHistory(data){
	
	$.ajax({
		url: "/resumes/" + $("#resumepk").val() +"/workhistory/add/",
		beforeSend: function(xhr){xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))},
		context: document.body,
		data: data,
		dataType: "json",
		type: "POST",
	}).done(function(data) {
		//It worked
		addWorkHistoryHTML(false, data[0].pk);
		//$( this ).addClass( "done" );
	}).fail(function() {
		//alert("it says it failed");
		//$( this ).addClass( "done" );
	}).always(function() {
		//$( this ).addClass( "done" );
	});

}

/*
 * function: addWorkHistoryHTML
 * prereqs: the degree global variable is updated
 */
function addWorkHistoryHTML(readOnly, employerID){
	
	$('#newjob').html('');
	savedjobsdiv = $("#savedjobs");
	
	toAppend='<div id=\"job'+employerID+ '\"\">';
	toAppend+='<h3><strong>' + job.title+'';
	if(!readOnly){
		toAppend+='<button type=\"button\" id=\"remjobbutton'+employerID+ '\" class=\"btn-default\" ><span class=\"glyphicon glyphicon-remove-sign\"></span></button>';
	}
	toAppend+='<h4>'+job.company;
	toAppend+='</h4>';
	toAppend+='<h4><small>'+job.startdate+ ' - ' + job.enddate + '</small></h4>';
	toAppend+="<textarea class=\"form-control savedtextarea\" id=\"jobfunctions_jobid_"+employerID+"\" >" + job.jobfunctions + "</textarea>";
	
	savedjobsdiv.append(toAppend);
	if(!readOnly){
		$("#remjobbutton"+employerID).toggleClass('pull-right');
		$("#remjobbutton"+employerID).hover(function (){
			$(this).toggleClass('btn-danger');
		});
		$("#remjobbutton"+employerID).click(function (){
			
			thistext = this.id;
			toRemove = 'remjobbutton';
			realEmployerID = thistext.replace(toRemove,'');
			
			//necessary because bootbox becomes the new "this"
			thisempl=this;
			
			bootbox.confirm("Are you sure you want to remove this work history from your resume?", function(result) {

				if (result==true){
					deleteWorkHistory(realEmployerID);
					$(thisempl).parent().closest('div').remove();
				}
			
			});
			
		});
	}
	$( "*" ).animate({"opacity": 1},200);
	$( "*" ).attr('disabled', false);
	
	empllist.push(job);
	jobcount++;
	$("#nojobs").html('');

}

function deleteWorkHistory(employerID){
	
	$.ajax({
		url: "/resumes/" + $("#resumepk").val() +"/workhistory/delete/"+employerID+"/",
		beforeSend: function(xhr){xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))},
		type: "DELETE",
	}).done(function() {
		--jobcount;
		if(jobcount==0){
			$("#nojobs").html(nojobstext);
		}
		//alert("it says it worked");
		//$( this ).addClass( "done" );
	}).fail(function() {
		//alert("it says it failed");
		//$( this ).addClass( "done" );
	}).always(function() {
		//$( this ).addClass( "done" );
	});

}

function createSkill(data){
	
	$.ajax({
		url: "/resumes/" + $("#resumepk").val() +"/skill/add/",
		beforeSend: function(xhr){xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))},
		context: document.body,
		data: data,
		dataType: "json",
		type: "POST",
	}).done(function(data) {
		//It worked
		addSkillHTML(false, data[0].pk);
		//$( this ).addClass( "done" );
	}).fail(function() {
		//alert("it says it failed");
		//$( this ).addClass( "done" );
	}).always(function() {
		//$( this ).addClass( "done" );
	});

}


function addSkillHTML(readOnly, skillID){
	
	newskill=$('#newskill');
	newskill.html("");
	savedskillsdiv = $("#savedskills");
	
	if(skilllist.length==0){ savedskillsdiv.append("<br/>"); } else {	savedskillsdiv.append(" ");	}
	
	if(!readOnly){
		skillhtml = "<button id=\'delskillbutton"+skillID+"\' type=\"button\" class=\"skillbtns btn btn-default\" >"+skill.skill+" <span id=\"delskillspan\" class=\"glyphicon glyphicon-remove\"></span></button>";
	}else{
		skillhtml = "<button id=\'skillbutton"+skillID+"\' type=\"button\" class=\"skillbtns btn btn-default\" >"+skill.skill+"</button>";
	}
	savedskillsdiv.append(skillhtml);
	
	if(!readOnly){
		$( "#delskillbutton"+skillID+"" ).click(function() {	
			
			thistext = this.id;
			toRemove = 'delskillbutton';
			realSkillID = thistext.replace(toRemove,'');
			
			deleteSkill(realSkillID);
			$(this).remove();
			
		});
		
		$(".skillbtns").hover(
			function () {
				$(this).addClass("btn-danger");
			},
	    	function () {
	    		$(this).removeClass("btn-danger");
	    	}
		);
	}else{
		$(".skillbtns").hover(
				function () {
					$(this).addClass("btn-info");
				},
		    	function () {
		    		$(this).removeClass("btn-info");
		    	}
		);
	}
	$( "*" ).animate({"opacity": 1},200);
	$( "*" ).attr('disabled', false);
	
	skilllist.push(skill);
	numskills++;
	$("#noskills").html('');
	
}

function deleteSkill(skillID){
	
	$.ajax({
		url: "/resumes/" + $("#resumepk").val() +"/skill/delete/"+skillID+"/",
		beforeSend: function(xhr){xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))},
		type: "DELETE",
	}).done(function() {
		--numskills;
		if(numskills==0){
			$("#noskills").html(noskillstext);
		}
		/*skilllist.pop(skill);
		if(skilllist.length==0){
			//reset the html
			savedskillsdiv.html("");
		}*/
		//alert("it says it worked");
		//$( this ).addClass( "done" );
	}).fail(function() {
		//alert("it says it failed");
		//$( this ).addClass( "done" );
	}).always(function() {
		//$( this ).addClass( "done" );
	});

}

function createCert(data){
	
	$.ajax({
		url: "/resumes/" + $("#resumepk").val() +"/cert/add/",
		beforeSend: function(xhr){xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))},
		context: document.body,
		data: data,
		dataType: "json",
		type: "POST",
	}).done(function(data) {
		//It worked
		addCertHTML(false, data[0].pk);
		//$( this ).addClass( "done" );
	}).fail(function() {
		//alert("it says it failed");
		//$( this ).addClass( "done" );
	}).always(function() {
		//$( this ).addClass( "done" );
	});

}

function addCertHTML(readOnly, certID){
	
	$('#newcert').html('');
	
	savedcertsdiv = $('#savedcerts');
	
	toAppend='<div id=\"cert'+certcount+ '\"\">';
	toAppend+='<h3><strong>' + cert.name+'';
	
	if(!readOnly){
		toAppend+='<button type=\"button\" id=\"remcertbutton'+certID+ '\" class=\"btn-default\" ><span class=\"glyphicon glyphicon-remove-sign\"></span></button>';
	}
	
	toAppend+='<h4>'+ cert.authority + ', ' + cert.licnumber + '</h4>';
	if(cert.url.length > 0){
		toAppend+='<h4>' + cert.url + '</h4>';
	}
	if (cert.neverexp){
		toAppend+='<h4><small>Expires: Never</small></h4>';	
	}else{
		toAppend+='<h4><small>Expires: '+ cert.expdate + '</small></h4>';
	}
	
	savedcertsdiv.append(toAppend);
	
	if(!readOnly){
		
		$("#remcertbutton"+certID).toggleClass('pull-right');
		$("#remcertbutton"+certID).click(function (){
			
			thistext = this.id;
			toRemove = 'remcertbutton';
			realCertID = thistext.replace(toRemove,'');
			
			//necessary because bootbox becomes the new "this"
			thiscert=this;
			
			bootbox.confirm("Are you sure you want to remove this certification from your resume?", function(result) {

				if (result==true){
					deleteCert(realCertID);
					$(thiscert).parent().closest('div').remove();
				}
			
			});
			
		});
	
	}
	
	$( "*" ).animate({"opacity": 1},200);
	$( "*" ).attr('disabled', false);
	
	certlist.push(cert);
	certcount++;
	$("#nocerts").html('');
}

function deleteCert(certID){
	
	$.ajax({
		url: "/resumes/" + $("#resumepk").val() +"/cert/delete/"+certID+"/",
		beforeSend: function(xhr){xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))},
		type: "DELETE",
	}).done(function() {
		--certcount;
		if(certcount==0){
			$("#nocerts").html(nocertstext);
		}
		//alert("it says it worked");
		//$( this ).addClass( "done" );
	}).fail(function() {
		//alert("it says it failed");
		//$( this ).addClass( "done" );
	}).always(function() {
		//$( this ).addClass( "done" );
	});

}

//add Certification Event Handler
$(document).ready(function() {
		$("#editemail").click(editEmail);
		$("#editmajor").click(editMajor);
        $("#addsummary").click(addSummary);
        $("#adddegree").click(addDegree);
        $("#addjob").click(addJob);
        $("#addskill").click(addSkill);
        $("#addcert").click(addCert);
        $( "*" ).attr('disabled', false);
});

var nosummarytext="<p><h4><br/>---Not added yet---<br/><br/></h4></p>";
function loadInitSummary(readOnly, resumeJSON){

	resume = jQuery.parseJSON(JSON.stringify(resumeJSON))[0];
	objective = resume.fields.objective;
	
	if(objective.length > 0){
		
		summary=$('#summary');
		
		summary.append("<br />");
		summary.append("<textarea id=\'summarytext\' class='form-control' ></textarea>");
		summary.append("<br />");
		
		if(!readOnly){
		
			summary.append("<p><button type=\"button\" id=\"savesummarybutton\" class=\"btn btn-primary\" ><span id=\"savesummbuttonspan\" class=\"glyphicon glyphicon-ok\"></span> Save</button> <button id=\'cancelsummarybutton\' type=\"button\" class=\"btn btn-default\" ><span class=\"glyphicon glyphicon-remove\"></span> Cancel</button></p>");
			
			$("#savesummarybutton").hide();
			$("#cancelsummarybutton").hide();
			
			addsummarybutton=$('#addsummary');
			addsummarybutton.html('<span class=\"glyphicon glyphicon-pencil\"></span>');
			addsummarybutton.show();
			
			$("#summarybtns").append('<button type=\"button\" id=\"remsummarybutton\" class=\"modbuttons summarybtn btn-lg\" ><span class=\"glyphicon glyphicon-remove-sign\"></span></button>')
			addsummarybutton.toggleClass('modbuttons');
			$("#summarybtns").toggleClass('pull-right');
			
			$("#remsummarybutton").click(function (){
				addsummarybutton.html('<span class=\"glyphicon glyphicon-plus-sign\"></span> Add Summary');
				//Move back to the left
				$("#summarybtns").toggleClass('pull-right');
				//Remove transparency
				addsummarybutton.toggleClass('modbuttons');
				addsummarybutton.show();
				summarydiv = $("#summary");
				summarydiv.html("");
				to_json = {
						"fieldname": "objective",
				        "fieldval": "",
				};
				updateResume(to_json)
				$("#remsummarybutton").remove();
				$("#nosummary").html(nosummarytext);
				
			});
		
		}
		
		summarytext = $("#summarytext");
	    summarytext.val( objective );
		summarytext.attr('readonly', true);
		summarytext.toggleClass('savedtextarea');
		
	}else{
		$("#nosummary").html(nosummarytext);
	}
	
}

var noeducationtext="<p><h4><br/>---Not added yet---<br/><br/></h4></p>";
function loadInitDeg(readOnly, degrees){
	
	degreesArr = jQuery.parseJSON(JSON.stringify(degrees));
	
	
	for(i = 0; i < degreesArr.length; ++i){
	
		degree.degreetype = degreesArr[i].fields.degreetype;
		degree.major = degreesArr[i].fields.major;
		degree.university = degreesArr[i].fields.university;
		degree.date = degreesArr[i].fields.date;
		degree.gpa = degreesArr[i].fields.gpa;
		degree.honors = degreesArr[i].fields.honors;
		
		addDegreeHTML(readOnly, degreesArr[i].pk);
		
	}
	
}

var nojobstext="<p><h4><br/>---Not added yet---<br/><br/></h4></p>";
function loadInitEmpls(readOnly, employers){
	
	employersArr = jQuery.parseJSON(JSON.stringify(employers));

	for(i = 0; i < employersArr.length; ++i){
	
		job = {
				title:employersArr[i].fields.title,
				company:employersArr[i].fields.company,
				jobfunctions:employersArr[i].fields.jobfunctions,
				startdate:employersArr[i].fields.startdate,
				enddate:employersArr[i].fields.enddate,
		}
		
		addWorkHistoryHTML(readOnly, employersArr[i].pk);
		
	}
		    
}

var noskillstext="<p><h4><br/>---Not added yet---<br/><br/></h4></p>";
function loadInitSkills(readOnly, skills){
	
	skillArr = jQuery.parseJSON(JSON.stringify(skills));

	for(i = 0; i < skillArr.length; ++i){
	
		skill = {
				skill:skillArr[i].fields.skill,
		}		
		addSkillHTML(readOnly, skillArr[i].pk);
		
	}
		    
}

var nocertstext="<p><h4><br/>---Not added yet---<br/><br/></h4></p>";
function loadInitCerts(readOnly, certs){
	
	certsArr = jQuery.parseJSON(JSON.stringify(certs));
	
	for(i = 0; i < certsArr.length; ++i){
	
		cert.name = certsArr[i].fields.name;
        cert.authority = certsArr[i].fields.authority;
        cert.licnumber = certsArr[i].fields.licnumber;
        cert.url = certsArr[i].fields.url;
        cert.expdate = certsArr[i].fields.expdate;
        cert.neverexp = certsArr[i].fields.neverexp;	
        
        addCertHTML(readOnly, certsArr[i].pk);
        
	}		    
}

function addSummary(){

	addsummarybutton=$('#addsummary');
	addsummarybutton.hide();
	
	summary=$('#summary');
	
	var summarytext = $("#summarytext");
	var summarytext_orig_val=summarytext.val();
	
	if(summarytext.val()){
	
		addsummarybutton.show();
		//summary.html(summary_orig_html);
		
		//Do not use animiate here because it has unforeseen consequences with datepicker styling
		$('#summary').parents().siblings().css({"opacity": .3});
		$(':input').not('#summary :input').attr('disabled', true);
		
		$("#savesummarybutton").show();
		$("#cancelsummarybutton").show();
			
		summarytext.attr('readonly', false);
		//summarytext.toggleClass('savedtextarea');
		summarytext.focus();
		    
	}else{
	
		summary.append("<br />");
		summary.append("<textarea id=\'summarytext\' class='form-control' ></textarea>");
		summary.append("<br />");
		summary.append("<p><button type=\"button\" id=\"savesummarybutton\" class=\"btn btn-primary\" ><span id=\"savesummbuttonspan\" class=\"glyphicon glyphicon-ok\"></span> Save</button> <button id=\'cancelsummarybutton\' type=\"button\" class=\"btn btn-default\" ><span class=\"glyphicon glyphicon-remove\"></span> Cancel</button></p>");
		
		$('#summary').parents().siblings().css({
	    	"opacity": .3
	    });
	    $(':input').not('#summary :input').attr('disabled', true);

	}
	    
    $("#savesummarybutton").click(function (){
        
        var summarytext = $("#summarytext");
		if(summarytext.val().length > 0){
		
			summarytext.attr('readonly', true);
			summarytext.toggleClass('savedtextarea');
			summarytext.focus();
			
			$("#savesummarybutton").hide();
			$("#cancelsummarybutton").hide();
			
			addsummarybutton.html('<span class=\"glyphicon glyphicon-pencil\"></span>');
			addsummarybutton.show();
			
			if($("#remsummarybutton").html()==undefined){				
				$("#summarybtns").append('<button type=\"button\" id=\"remsummarybutton\" class=\"modbuttons summarybtn btn-lg\" ><span class=\"glyphicon glyphicon-remove-sign\"></span></button>')
				addsummarybutton.toggleClass('modbuttons');
				$("#summarybtns").toggleClass('pull-right');
				
				$("#remsummarybutton").click(function (){
					addsummarybutton.html('<span class=\"glyphicon glyphicon-plus-sign\"></span> Add Summary');
					//Move back to the left
					$("#summarybtns").toggleClass('pull-right');
					//Remove transparency
					addsummarybutton.toggleClass('modbuttons');
					addsummarybutton.show();
					summarydiv = $("#summary");
					summarydiv.html("");
					to_json = {
							"fieldname": "objective",
					        "fieldval": "",
					};
					updateResume(to_json)
					$("#remsummarybutton").remove();
					$("#nosummary").html(nosummarytext);
					
				});
			}
						
			//Saving
			summarytext_orig_val=summarytext.val();
			
			to_json = {
					"fieldname": "objective",
			        "fieldval": summarytext.val()
			};
			updateResume(to_json)
			$("#nosummary").html('');
			
			
		}else{
			
			summary = $("#summary");
			summary.prepend('<div id="nosummary" class="alert alert-danger fade in"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>'+
							'<strong>There\'s nothing to save dude!</strong></div>');
			setTimeout(function(){
				$("#nosummary").alert('close');
			},3000);
		
		}
		$( "*" ).animate({"opacity": 1},200);
		$( "*" ).attr('disabled', false);

	});
	$("#cancelsummarybutton").click(function (){
		
		addsummarybutton.show();
		
		if(summarytext_orig_val){		
			summarytext.val(summarytext_orig_val);
			$("#savesummarybutton").hide();
			$("#cancelsummarybutton").hide();
						
		}else{
			
			summarydiv = $("#summary");
			summarydiv.html("");
			$("#nosummary").html(nosummarytext);
			
		}
		
		$( "*" ).animate({
			"opacity": 1
		},200);
		$( "*" ).attr('disabled', false);
	});
     
}

function addDegree(){

	adddegreebutton=$('#adddegree');
	
    newdegree=$('#newdegree');
	
	newdegree.append("<br />");
	newdegree.append("<form class=\"form-inline\" role=\"form\"><div class=\"form-group\">");
	newdegree.append("<div class=\"row\">");
	newdegree.append("<div><label for=\"newdegreetype\" class=\"col-xs-2 control-label\">*Degree Type</label><div class=\"col-sm-3\"><input id=\"newdegreetype\" type=\"text\" class=\"form-control\" placeholder=\"i.e. B.S., B.A.\"></div></div>");
	newdegree.append("<div><label for=\"newdegreemajor\" class=\"col-xs-1 control-label\">*Major</label><div class=\"col-sm-3\"><input id=\"newdegreemajor\" type=\"text\" class=\"form-control\" placeholder=\"i.e. Computer Science\"></div></div>");
	newdegree.append("</div>");
	newdegree.append("<div class=\"row\">");
	newdegree.append("<div><label for=\"newdegreeuniv\" class=\"col-xs-2 control-label\">*University</label><div class=\"col-sm-3\"><input id=\"newdegreeuniv\" type=\"text\" class=\"form-control\" placeholder=\"i.e. Auburn University\"></div></div>");
	newdegree.append("<div><label for=\"newdegreegpa\" class=\"col-xs-1 control-label\">GPA</label><div class=\"col-sm-3\"><input id=\"newdegreegpa\" type=\"text\" class=\"form-control\" placeholder=\"3.0\"></div></div>");
	newdegree.append("</div>");
	newdegree.append("<div class=\"row\">");
	newdegree.append("<div><label for=\"newdegreegrad\" class=\"col-xs-2 control-label\">*Graduation Date</label><div class=\"col-sm-3\"><input id=\"newdegreegrad\" type=\"text\" ></div></div>");
	newdegree.append("<div><label for=\"newdegreehonors\" class=\"col-xs-1 control-label\">Honors</label><div class=\"col-sm-3\"><input id=\"newdegreehonors\" type=\"text\" class=\"form-control\" placeholder=\"Cum Laude\"></div></div>");
	newdegree.append("</div>");
	newdegree.append("<div class=\"row\">");
	newdegree.append("<div><p class=\"col-xs-2\">*Denotes required field</p></div>");
	newdegree.append("</div>");
	newdegree.append("<div class=\"row\">");
	newdegree.append("<p><button type=\"button\" id=\"savedegreebutton\" class=\"btn btn-primary\" ><span id=\"savedegreebuttonspan\" class=\"glyphicon glyphicon-ok\"></span> Save</button> <button id=\'canceldegreebutton\' type=\"button\" class=\"btn btn-default\" ><span class=\"glyphicon glyphicon-remove\"></span> Cancel</button></p>");
	newdegree.append("</div>");
	newdegree.append("</div></form><br />");
	
	//Do not use animiate here because it has unforeseen consequences with datepicker styling
	$('#newdegree').parents().siblings().css({
    	"opacity": .3
    });
    adddegreebutton.css({"opacity": .3});
    
    $(':input').not('#newdegree :input').attr('disabled', true);
    
    var searchMinDate = "-50y";
	var searchMaxDate = "+10y";
	/*if ((new Date()).getDate() <= 5) {
    	searchMaxDate = "-2m";
	}*/

	$("#newdegreegrad").datepicker({
	    showOn: 'both', 
	    buttonImage: '/static/images/calendar.gif',
    	dateFormat: "M yy",
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
	    	setTimeout(function(){$("#newdegreegrad").focus();},50);
        	
        	//In some cases the opacity is still set to 0.3 so lets ensure that the calendar looks correct
	    	$("#ui-datepicker-div").css({opacity: 1});
	    	
			if ((datestr = $("#newdegreegrad").val()).length > 0) {
		        var year = datestr.substring(datestr.length - 4, datestr.length);
		        var month = datestr.substring(0, 2);
		        $("#newdegreegrad").datepicker('option', 'defaultDate', new Date(year, month, 1));
		        $("#newdegreegrad").datepicker('setDate', new Date(year, month, 1));
	        }
	    },
	    onClose: function (input, inst) {
	            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
	            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
	            $("#newdegreegrad").datepicker('option', 'defaultDate', new Date(year, month, 1));
	            $("#newdegreegrad").datepicker('setDate', new Date(year, month, 1));
	    },
    });
    
    //Remove previous datepicker styling
	$("#dpcalcss").remove();
	$("#dpcurrprevnext").remove();
	$("#dpbutton").remove();
	
	//Add new styling
    $('<style id="dpcalcss" type="text/css"> .ui-datepicker-calendar { display: none !important; } </style>').appendTo("head");
	$('<style id="dpcurrprevnext" type="text/css"> .ui-datepicker-current, .ui-datepicker-next, .ui-datepicker-prev { display: none; } </style>').appendTo("head");
	$('<style id="dpbutton" type="text/css"> .ui-datepicker-buttonpane button { float: left; } </style>').appendTo("head");
	
	$("#newdegreegrad").focus(function () {
		$("#ui-datepicker-div").position({
			my: "center top",
			at: "center bottom",
			of: $(this)
		});
	});

	    
    $("#savedegreebutton").click(function (){
        
		degree.degreetype = $("#newdegreetype").val();
		degree.major = $("#newdegreemajor").val();
		degree.university = $("#newdegreeuniv").val();
		degree.date = $("#newdegreegrad").val();
		degree.gpa = $("#newdegreegpa").val();
		degree.honors = $("#newdegreehonors").val();

		if(degree.degreetype.length == 0){	$("#newdegreetype").parent().parent().addClass("has-error"); return; } else{ $("#newdegreetype").parent().parent().removeClass("has-error"); }
		if(degree.major.length == 0){	$("#newdegreemajor").parent().parent().addClass("has-error"); return; 	} else{ $("#newdegreemajor").parent().parent().removeClass("has-error"); }
		if(degree.university.length == 0){	$("#newdegreeuniv").parent().parent().addClass("has-error"); return; 	} else{ $("#newdegreeuniv").parent().parent().removeClass("has-error"); }
		if(degree.date.length == 0){	$("#newdegreegrad").parent().parent().addClass("has-error"); return; 	} else{ $("#newdegreegrad").parent().parent().removeClass("has-error"); }
		
		createDegree(degree);
    	
	});
	$("#canceldegreebutton").click(function (){
		
		$('#adddegree').show();
		$('#newdegree').html('');
	
		$( "*" ).animate({
			"opacity": 1
		},200);
		$( "*" ).attr('disabled', false);
	});
     
}

function addCert(){

	newcert=$('#newcert');
	
	newcert.append("<br />");
	newcert.append("<form class=\"form-inline\" role=\"form\"><div class=\"form-group\">");
	newcert.append("<div class=\"row\">");
	newcert.append("<div><label for=\"newcertname\" class=\"col-xs-2 control-label\">*Certification Name</label><div class=\"col-sm-4\"><input id=\"newcertname\" type=\"text\" class=\"form-control\" placeholder=\"Java Level II\"></div></div>");
	newcert.append("</div>");
	newcert.append("<div class=\"row\">");
	newcert.append("<div><label for=\"newcertauth\" class=\"col-xs-2 control-label\">*Certification Authority</label><div class=\"col-sm-4\"><input id=\"newcertauth\" type=\"text\" class=\"form-control\" placeholder=\"Oracle\"></div></div>");
	newcert.append("</div>");
	newcert.append("<div class=\"row\">");
	newcert.append("<div><label for=\"newcertlicnum\" class=\"col-xs-2 control-label\">*License Number</label><div class=\"col-sm-4\"><input id=\"newcertlicnum\" type=\"text\" class=\"form-control\" placeholder=\"\"></div></div>");
	newcert.append("</div>");
	newcert.append("<div class=\"row\">");
	newcert.append("<div><label for=\"newcerturl\" class=\"col-xs-2 control-label\">URL</label><div class=\"col-sm-6\"><input id=\"newcerturl\" type=\"text\" class=\"form-control\" placeholder=\"\"></div></div>");
	newcert.append("</div>");
	newcert.append("<div class=\"row\">");
	newcert.append("<div><label for=\"newcertexpdate\" class=\"col-xs-2 control-label\">*Exp Date</label><div class=\"col-sm-2\"><input id=\"newcertexpdate\" type=\"text\" class=\"form-control\" placeholder=\"\"></div><label class=\"col-xs-1 control-label\">Never Expires</label><div class=\"col-sm-1\"><input id=\"newcertexp\" type=\"checkbox\" class=\"form-control\" /></div></div>");
	newcert.append("</div>");
	newcert.append("<div class=\"row\">");
	newcert.append("<div><p class=\"col-xs-2\">*Denotes required field</p></div>");
	newcert.append("</div>");
	newcert.append("<div class=\"row\">");
	newcert.append("<p><button type=\"button\" id=\"savecertbutton\" class=\"btn btn-primary\" ><span class=\"glyphicon glyphicon-ok\"></span> Save</button> <button id=\'cancelcertbutton\' type=\"button\" class=\"btn btn-default\" ><span class=\"glyphicon glyphicon-remove\"></span> Cancel</button></p>");
	newcert.append("</div>");
	newcert.append("</div></form><br />");
	
	$('#newcert').parents().siblings().css({
    	"opacity": .3
    });
    
    $(':input').not('#newcert :input').attr('disabled', true);
	
    $("#newcertexp").click(function (){
    	if($(this).prop('checked')){
        	$( "#newcertexpdate" ).attr('disabled', true);
        	$( "#newcertexpdate" ).val("");
        	$( "#newcertexpdate" ).animate({
    			"opacity": 0.5
    		},200);
    	}else{
        	$( "#newcertexpdate" ).attr('disabled', false);
        	$( "#newcertexpdate" ).animate({
    			"opacity": 1
    		},200);
    	}
    });
    
    $("#newcertexpdate").datepicker({
		minDate: "0d",
	    maxDate: "+15y",
	    changeMonth: true,
	    changeYear: true,
	    beforeShow: function() {
	    	//Weird Datepicker Quirk. You have to use a timeout before setting the focus or you get a recursion error. You also can't use this because
	    	//for some reason this is not set to the correct object after the first selection	    	
	    	setTimeout(function(){
	    		$("#newcertexpdate").focus();
	    	},50);
	    	//In some cases the opacity is still set to 0.3 so lets ensure that the calendar looks correct
	    	$("#ui-datepicker-div").css({opacity: 1});
	    	
	    },onClose: function (input, inst) {
	    	$("#newcertexpdate").datepicker('option', 'defaultDate', input);
	        $("#newcertexpdate").datepicker('setDate', input);
	    },
	});
	
	//Remove previous datepicker styling
	$("#dpcalcss").remove();
	$("#dpcurrprevnext").remove();
	$("#dpbutton").remove();
	
	$('<style id="dpcurrprevnext" type="text/css"> .ui-datepicker-current, .ui-datepicker-next, .ui-datepicker-prev { display: none; } </style>').appendTo("head");
	
	$("#newcertexpdate").focus(function () {
		$("#ui-datepicker-div").position({
			my: "center top",
			at: "center bottom",
			of: $(this)
		});	
	});
	
	$("#savecertbutton").click(function (){
        
        cert.name = $("#newcertname").val();
        cert.authority = $("#newcertauth").val();
        cert.licnumber = $("#newcertlicnum").val();
        cert.url = $("#newcerturl").val();
        cert.expdate = $("#newcertexpdate").val();
        cert.neverexp = $("#newcertexp").prop('checked');	
        
        if(cert.name.length == 0){	$("#newcertname").parent().parent().addClass("has-error"); return; } else{ $("#newcertname").parent().parent().removeClass("has-error"); }
		if(cert.authority.length == 0){	$("#newcertauth").parent().parent().addClass("has-error"); return; 	} else{ $("#newcertauth").parent().parent().removeClass("has-error"); }
		if(cert.licnumber.length == 0){	$("#newcertlicnum").parent().parent().addClass("has-error"); return; 	} else{ $("#newcertlicnum").parent().parent().removeClass("has-error"); }
		if(cert.expdate.length == 0 && cert.neverexp == "False"){	$("#newcertexpdate").parent().parent().addClass("has-error"); return; 	} else{ $("#newcertexpdate").parent().parent().removeClass("has-error"); }
		
		createCert(cert);
		
	});
	
	$("#cancelcertbutton").click(function (){
		
		$('#addcert').show();
		$('#newcert').html('');
	
		$( "*" ).animate({
			"opacity": 1
		},200);
		$( "*" ).attr('disabled', false);
	});
	
}

function addSkill(){
	
	newskill=$('#newskill');
	newskill.append("<form class=\"form-inline\" role=\"form\"><div class=\"form-group\">");
	newskill.append("<div class=\"row\">");
	newskill.append("<div><label for=\"skill\" class=\"col-sm-1 control-label\">Skill/Course</label><div class=\"col-sm-4\"><input id=\"skill\" type=\"text\" class=\"form-control\" placeholder=\"i.e. HTML5, Being Awesome\"></div></div></div>");
	newskill.append("<p><button type=\"button\" id=\"saveskillbutton\" class=\"btn btn-primary\" ><span id=\"saveskillbuttonspan\" class=\"glyphicon glyphicon-ok\"></span> Save</button> <button id=\'cancelskillbutton\' type=\"button\" class=\"btn btn-default\" ><span class=\"glyphicon glyphicon-remove\"></span> Cancel</button></p>");
	newskill.append("</div>");
	
	//Do not use animiate here because it has unforeseen consequences with datepicker styling
	$('#skilljob').parents().siblings().css({
    	"opacity": .3
    });
    $(':input').not('#newskill :input').attr('disabled', true);
    
    $( "#saveskillbutton" ).click(function() {
	
    	skill.skill = $("#skill").val();
		if(skill.skill.length == 0){	$("#skill").parent().parent().addClass("has-error"); return; } else{ $("#skill").parent().parent().removeClass("has-error"); }
		createSkill(skill);
		
	});
	
	$( "#cancelskillbutton" ).click(function() {
	
		newskill.html("");
		
		$( "*" ).animate({
			"opacity": 1
		},200);
		$( "*" ).attr('disabled', false);
			
	});
		
}

function addJob(){
	
	newjob=$('#newjob');
	
	newjob.append('<p>');
	newjob.append("<form class=\"form-inline\" role=\"form\"><div class=\"form-group\">");
	newjob.append("<div class=\"row\">");
	newjob.append("<div><label for=\"newjobtitle\" class=\"col-xs-2 control-label\">*Job Title</label><div class=\"col-sm-3\"><input id=\"newjobtitle\" type=\"text\" class=\"form-control\" placeholder=\"i.e. Software Engineer\"></div></div></div>");
	newjob.append("<div class=\"row\">");
	newjob.append("<div><label for=\"newjobconame\" class=\"col-xs-2 control-label\">*Company</label><div class=\"col-sm-3\"><input id=\"newjobconame\" type=\"text\" class=\"form-control\" ></div></div></div>");
	newjob.append("<div class=\"row\">");
	newjob.append("<div><label for=\"jobfunctions\" class=\"col-xs-2 control-label\">*Job Functions</label><div class=\"col-sm-3\"><textarea id=\"jobfunctions\" type=\"text\" class=\"form-control\" /></div></div></div>");
	newjob.append("<div class=\"row\">");
	newjob.append('<div><br/><label for=\"startdate\" class=\"col-xs-2 control-label\">Date Range</label><input id=\'startdate\' size=12 type=\'text\' readonly=\'readonly\' /> - <input id=\'enddate\' size=12 type=\'text\' readonly=\'readonly\' /></div>');
	newjob.append('<p id=\'ispresentp\'><input id=\'ispresent\' type=\'checkbox\' /> Present</p>');
	newjob.append("</div>");
	newjob.append("<div class=\"row\">");
	newjob.append("<div><p class=\"col-xs-2\">*Denotes required field</p></div>");
	newjob.append("</div>");
	newjob.append("<div class=\"row\">");
	newjob.append("<p><button type=\"button\" id=\"savejobbutton\" class=\"btn btn-primary\" ><span id=\"savejobbuttonspan\" class=\"glyphicon glyphicon-ok\"></span> Save</button> <button id=\'canceljobbutton\' type=\"button\" class=\"btn btn-default\" ><span class=\"glyphicon glyphicon-remove\"></span> Cancel</button></p>");
	newjob.append("</div>");
	newjob.append('</form></p>');
	
	$("#ispresent").click(function() {
	    if($(this).prop('checked')){
        	$( "#enddate" ).attr('disabled', true);
        	$( "#enddate" ).val("");
        	$( "#enddate" ).animate({
    			"opacity": 0.5
    		},200);
    	}else{
        	$( "#enddate" ).attr('disabled', false);
        	$( "#enddate" ).animate({
    			"opacity": 1
    		},200);
    	}
	});
	
	//Change the opacity except for anything starting with ui-datepicker
	$('#newjob').parents().siblings().not($("[id^=ui-datepicker]")).animate({
    	"opacity": .3
    },200);
    $('#addjob').animate({"opacity": .3},200);
    
    $(':input').not('#newjob :input').attr('disabled', true);
    
    $( "#savejobbutton" ).click(function() {
	
		if($("#ispresent").prop('checked')){
			$( "#enddate" ).val("Present");
		}
		
		job.title = $("#newjobtitle").val();
		job.company = $("#newjobconame").val();
		job.jobfunctions = $("#jobfunctions").val();
		job.startdate = $("#startdate").val();
		job.enddate = $("#enddate").val();
		
		if(job.title.length == 0){	$("#newjobtitle").parent().parent().addClass("has-error"); return; } else{ $("#newjobtitle").parent().parent().removeClass("has-error"); }
		if(job.company.length == 0){	$("#newjobconame").parent().parent().addClass("has-error"); return; } else{ $("#newjobconame").parent().parent().removeClass("has-error"); }
		if(job.jobfunctions.length == 0){	$("#jobfunctions").parent().parent().addClass("has-error"); return; } else{ $("#jobfunctions").parent().parent().removeClass("has-error"); }
		if(job.startdate.length > 0 && job.enddate.length == 0){ $("#enddate").parent().addClass("has-error"); return; } else{ $("#enddate").parent().removeClass("has-error"); }
		
		createWorkHistory(job);
		
	});
	
	$( "#canceljobbutton" ).click(function() {
	
		newjob.html("");
		
		$( "*" ).animate({
			"opacity": 1
		},200);
		$( "*" ).attr('disabled', false);
			
	});
	
	var searchMinDate = "-50y";
	var searchMaxDate = "0m";
	if ((new Date()).getDate() <= 5) {
    	searchMaxDate = "-2m";
	}

	$("#startdate").datepicker({
	    showOn: 'both', 
    	buttonImage: '/static/images/calendar.gif',
    	dateFormat: "M yy",
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
	    	
			if ((datestr = $("#startdate").val()).length > 0) {
		    	var year = datestr.substring(datestr.length - 4, datestr.length);
		    	var month = datestr.substring(0, 2);
		        $("#startdate").datepicker('option', 'defaultDate', new Date(year, month, 1));
		        $("#startdate").datepicker('setDate', new Date(year, month, 1));
		    }
	    },
	    onClose: function (input, inst) {
	            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
	            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
	            $("#startdate").datepicker('option', 'defaultDate', new Date(year, month, 1));
	            $("#startdate").datepicker('setDate', new Date(year, month, 1));
	            var to = $("#enddate").val();
	            $("#enddate").datepicker('option', 'minDate', new Date(year, month, 1));
	            if (to.length > 0) {
	                var toyear = to.substring(to.length - 4, to.length);
	                var month = to.substring(0, 2);
	                $("#enddate").datepicker('option', 'defaultDate', new Date(toyear, tomonth, 1));
	                $("#enddate").datepicker('setDate', new Date(toyear, tomonth, 1));
	            }
	    }
    });
	$("#startdate").focus(function () {
		//$(".ui-datepicker-calendar").hide();
		$("#ui-datepicker-div").position({
			my: "center top",
			at: "center bottom",
			of: $(this)
		});
	});
	
    $("#enddate").datepicker({
        showOn: 'both', 
    	buttonImage: '/static/images/calendar.gif',
    	dateFormat: "M yy",
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
	    	setTimeout(function(){$("#enddate").focus();},50);
	    	
	    	//In some cases the opacity is still set to 0.3 so lets ensure that the calendar looks correct
	    	$("#ui-datepicker-div").css({opacity: 1});
			        
            if ((datestr = $("#enddate").val()).length > 0) {
                var year = datestr.substring(datestr.length - 4, datestr.length);
                var month = datestr.substring(0, 2);
                $("#enddate").datepicker('option', 'defaultDate', new Date(year, month, 1));
                $("#enddate").datepicker('setDate', new Date(year, month, 1));
            }
        },
        onClose: function (input, inst) {
            var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
            var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
            $("#enddate").datepicker('option', 'defaultDate', new Date(year, month, 1));
            $("#enddate").datepicker('setDate', new Date(year, month, 1));
            var from = $("#startdate").val();
            $("#startdate").datepicker('option', 'maxDate', new Date(year, month, 1));
            if (from.length > 0) {
                var fryear = from.substring(from.length - 4, from.length);
                var frmonth = from.substring(0, 2);
                $("#startdate").datepicker('option', 'defaultDate', new Date(fryear, frmonth, 1));
                $("#startdate").datepicker('setDate', new Date(fryear, frmonth, 1));
            }

        }
    });
    
    $("#enddate").focus(function () {
		//$(".ui-datepicker-calendar").hide();
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
	
	enddateoffset = $("#enddate").offset();
	$("#ispresentp").offset({left:enddateoffset.left});
}