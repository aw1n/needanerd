//add Certification Event Handler
$(document).ready(function() {
        $("#nerdregbutton").click(function(){
        	window.location = "/students/register/"
        });
        $("#employerregbutton").click(function(){
        	window.location = "/employers/register/"
        });
        
});

function confirmDelete(userpk){

	bootbox.confirm("Are you sure you want to delete your entire account?", function(result) {		
		if (result==true){
			window.location = "/accounts/delete/"+userpk+"/"
		}
	});		
}