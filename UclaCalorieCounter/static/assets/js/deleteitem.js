function deleteFoodLog (item_id, portion){
	$.ajax({
	    url: "/delete/" + item_id + "/",
	    success: function(){
		if (portion <= 1)
		{
		$("#"+item_id).remove();
		}
		else
		{
		$("#portion"+item_id).html(portion-1);
		}
	    }
	});
}
