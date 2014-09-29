function deleteFoodLog (item_id){
	$.ajax({
	    url: "/delete/" + item_id + "/",
	    success: function(){
		{
		$("#"+item_id).remove();
		}
	    }
	});
}
