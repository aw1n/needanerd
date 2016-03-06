$(document).ready(function() {
	
	$("#studentlinkedin").click(studentLinkedInLogin);

});

function studentLinkedInLogin(){
	
	var CSRF_TOKEN = $("#csrf_token").val();
	var sRedirectURI = window.location;
	
	//Scope is optional https://developer.linkedin.com/docs/oauth2?u=0
	linkedinURL ="https://www.linkedin.com/uas/oauth2/authorization?response_type=code" +
			"&client_id=77ec2qizij7hrp&state="+CSRF_TOKEN+"&redirect_uri="+sRedirectURI+"";
	window.location = linkedinURL;

}