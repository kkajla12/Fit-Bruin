function updateportion (foodlog_id){
	$.ajax({
	    url: "/updateportion/" + foodlog_id + "/" + $("#portion"+foodlog_id).val() + "/",
	    success: function(){
		var value = $("#portion"+foodlog_id).val();
		$("#portion"+foodlog_id).val(value);
		alert( "Portion Updated." );
	    }
	});
}
