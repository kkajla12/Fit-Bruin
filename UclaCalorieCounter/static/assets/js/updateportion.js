function updateportion (foodlog_id){
	$.ajax({
	    url: "/updateportion/" + foodlog_id + "/" + $("#portion"+foodlog_id).val() + "/",
	});
}
