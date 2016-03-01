$(document).ready(function() {
	
	$("#studentlinkedin").click(studentLinkedInLogin);

});

function studentLinkedInLogin(){
	
	var CSRF_TOKEN = $("#csrf_token").val();
	var sRedirectURI = window.location;
	
	linkedinURL ="https://www.linkedin.com/uas/oauth2/authorization?response_type=code" +
			"&client_id=77psqp9utxoikh&scope=r_fullprofile&state="+CSRF_TOKEN+"&redirect_uri="+sRedirectURI+"";
	window.location = linkedinURL;

}