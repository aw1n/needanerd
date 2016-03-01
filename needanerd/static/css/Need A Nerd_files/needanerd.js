function confirmDelete(userpk){

	var r=confirm("Are you sure you want to delete your entire account");
	if (r==true){
		window.location = "/accounts/delete/"+userpk+"/"
	}	
}